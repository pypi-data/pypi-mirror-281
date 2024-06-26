# Copyright (c) Alibaba, Inc. and its affiliates.
# Copyright (c) OpenCompass.

import functools
import importlib
import os
import re
import random
import sys
from typing import Any, Union, Dict, List, Tuple, Optional, Set
import hashlib
import torch.nn.functional as F

import jsonlines as jsonl
import yaml

from llmuses.constants import DumpMode, OutputsStructure
from llmuses.utils.logger import get_logger
from transformers.utils import strtobool

logger = get_logger()

TEST_LEVEL_LIST = [0, 1]

# Example: export TEST_LEVEL_LIST=0,1
TEST_LEVEL_LIST_STR = 'TEST_LEVEL_LIST'


def test_level_list():
    global TEST_LEVEL_LIST
    if TEST_LEVEL_LIST_STR in os.environ:
        TEST_LEVEL_LIST = [
            int(x) for x in os.environ[TEST_LEVEL_LIST_STR].split(',')
        ]

    return TEST_LEVEL_LIST


def jsonl_to_list(jsonl_file):
    """
    Read jsonl file to list.

    Args:
        jsonl_file: jsonl file path.

    Returns:
        list: list of lines. Each line is a dict.
    """
    res_list = []
    with jsonl.open(jsonl_file, mode='r') as reader:
        for line in reader.iter(
                type=dict, allow_none=True, skip_invalid=False):
            res_list.append(line)
    return res_list


def jsonl_to_reader(jsonl_file):
    """
    Read jsonl file to reader object.

    Args:
        jsonl_file: jsonl file path.

    Returns:
        reader: jsonl reader object.
    """
    with jsonl.open(jsonl_file, mode='r') as reader:
        return reader


def jsonl_to_csv():
    pass


def dump_jsonl_data(data_list, jsonl_file, dump_mode=DumpMode.OVERWRITE):
    """
    Dump data to jsonl file.

    Args:
        data_list: data list to be dumped.  [{'a': 'aaa'}, ...]
        jsonl_file: jsonl file path.
        dump_mode: dump mode. It can be 'overwrite' or 'append'.
    """
    if not jsonl_file:
        raise ValueError('output file must be provided.')

    jsonl_file = os.path.expanduser(jsonl_file)

    if dump_mode == DumpMode.OVERWRITE:
        dump_mode = 'w'
    elif dump_mode == DumpMode.APPEND:
        dump_mode = 'a'
    with jsonl.open(jsonl_file, mode=dump_mode) as writer:
        writer.write_all(data_list)
    logger.info(f'Dump data to {jsonl_file} successfully.')


def yaml_to_dict(yaml_file) -> dict:
    """
    Read yaml file to dict.
    """
    with open(yaml_file, 'r') as f:
        try:
            stream = yaml.safe_load(f)
        except yaml.YAMLError as e:
            logger.error(f'{e}')
            raise e

    return stream


def get_obj_from_cfg(eval_class_ref: Any, *args, **kwargs) -> Any:
    module_name, spliter, cls_name = eval_class_ref.partition(':')

    try:
        obj_cls = importlib.import_module(module_name)
    except ImportError as e:
        logger.error(f'{e}')
        raise e

    if spliter:
        for attr in cls_name.split('.'):
            obj_cls = getattr(obj_cls, attr)

    return functools.partial(obj_cls, *args, **kwargs)


def markdown_table(header_l, data_l):
    md_str = f'| {" | ".join(header_l)} |'
    md_str += f'\n| {" | ".join(["---"] * len(header_l))} |'
    for data in data_l:
        if isinstance(data, str):
            data = [data]
        assert len(data) <= len(header_l)
        tmp = data + [''] * (len(header_l) - len(data))
        md_str += f'\n| {" | ".join(tmp)} |'
    return md_str


def random_seeded_choice(seed: Union[int, str, float], choices, **kwargs):
    """Random choice with a (potentially string) seed."""
    return random.Random(seed).choices(choices, k=1, **kwargs)[0]


def gen_hash(name: str):
    return hashlib.md5(name.encode(encoding='UTF-8')).hexdigest()


def dict_torch_dtype_to_str(d: Dict[str, Any]) -> dict:
    """
        Checks whether the passed dictionary and its nested dicts have a *torch_dtype* key and if it's not None,
        converts torch.dtype to a string of just the type. For example, `torch.float32` get converted into *"float32"*
        string, which can then be stored in the json format.

        Refer to: https://github.com/huggingface/transformers/pull/16065/files for details.
        """
    if d.get('torch_dtype', None) is not None and not isinstance(d['torch_dtype'], str):
        d['torch_dtype'] = str(d['torch_dtype']).split('.')[1]

    for value in d.values():
        if isinstance(value, dict):
            dict_torch_dtype_to_str(value)

    return d


def remove_objects_in_dict(d: Dict[str, Any]) -> dict:
    res = {}
    for k, v in d.items():
        if isinstance(v, (int, float, str, dict)):
            res[k] = str(v)

    return res


class ResponseParser:

    @staticmethod
    def parse_first_capital(text: str) -> str:
        for t in text:
            if t.isupper():
                return t
        return ''

    @staticmethod
    def parse_last_capital(text: str) -> str:
        for t in text[::-1]:
            if t.isupper():
                return t
        return ''

    @staticmethod
    def parse_first_option(text: str, options: str) -> str:
        """Find first valid option for text."""

        patterns = [
            f'[Tt]he answer is [{options}]',
            f'[Tt]he correct answer is [{options}]',
            f'答案是(.*?)[{options}]',
            f'答案为(.*?)[{options}]',
            f'固选(.*?)[{options}]',
            f'答案应该是(.*?)[{options}]',
            f'(\s|^)[{options}][\s。，,\.$]',  # noqa
            f'[{options}]',
        ]

        regexes = [re.compile(pattern) for pattern in patterns]
        for regex in regexes:
            match = regex.search(text)
            if match:
                outputs = match.group(0)
                for i in options:
                    if i in outputs:
                        return i
        return ''

    @staticmethod
    def parse_first_capital_multi(text: str) -> str:
        match = re.search(r'([A-D]+)', text)
        if match:
            return match.group(1)
        return ''

    @staticmethod
    def parse_last_option(text: str, options: str) -> str:
        match = re.findall(rf'([{options}])', text)
        if match:
            return match[-1]
        return ''


def make_outputs_dir(work_dir: str, model_id: str, model_revision: str, dataset_id: str):
    model_revision = model_revision if model_revision is not None else 'none'
    # now = datetime.datetime.now()
    # format_time = now.strftime('%Y%m%d_%H%M%S')
    # outputs_name = format_time + '_' + 'default' + '_' + model_id.replace('/', '_') + '_' + model_revision
    # outputs_dir = os.path.join(work_dir, outputs_name)
    dataset_name = dataset_id.replace('/', '_')
    outputs_dir = os.path.join(work_dir, dataset_name)

    return outputs_dir


def make_outputs_structure(outputs_dir: str):
    logs_dir = os.path.join(outputs_dir, 'logs')
    predictions_dir = os.path.join(outputs_dir, 'predictions')
    reviews_dir = os.path.join(outputs_dir, 'reviews')
    reports_dir = os.path.join(outputs_dir, 'reports')

    os.makedirs(outputs_dir, exist_ok=True)
    os.makedirs(logs_dir, exist_ok=True)
    os.makedirs(predictions_dir, exist_ok=True)
    os.makedirs(reviews_dir, exist_ok=True)
    os.makedirs(reports_dir, exist_ok=True)

    outputs_structure = {
        OutputsStructure.LOGS_DIR: logs_dir,
        OutputsStructure.PREDICTIONS_DIR: predictions_dir,
        OutputsStructure.REVIEWS_DIR: reviews_dir,
        OutputsStructure.REPORTS_DIR: reports_dir,
    }

    return outputs_structure


def import_module_util(import_path_prefix: str, module_name: str, members_to_import: list) -> dict:
    """
    Import module utility function.

    Args:
        import_path_prefix: e.g. 'llmuses.benchmarks.'
        module_name: The module name to import. e.g. 'mmlu'
        members_to_import: The members to import.
            e.g. ['DATASET_ID', 'SUBJECT_MAPPING', 'SUBSET_LIST', 'DataAdapterClass']

    Returns:
        dict: imported modules map. e.g. {'DATASET_ID': 'mmlu', 'SUBJECT_MAPPING': {...}, ...}
    """
    imported_modules = {}
    module = importlib.import_module(import_path_prefix + module_name)
    for member_name in members_to_import:
        imported_modules[member_name] = getattr(module, member_name)

    return imported_modules


def normalize_score(score: Union[float, dict], keep_num: int = 4) -> Union[float, dict]:
    """
    Normalize score.

    Args:
        score: input score, could be float or dict. e.g. 0.12345678 or {'acc': 0.12345678, 'f1': 0.12345678}
        keep_num: number of digits to keep.

    Returns:
        Union[float, dict]: normalized score. e.g. 0.1234 or {'acc': 0.1234, 'f1': 0.1234}
    """
    if isinstance(score, float):
        score = round(score, keep_num)
    elif isinstance(score, dict):
        score = {k: round(v, keep_num) for k, v in score.items()}
    else:
        logger.warning(f'Unknown score type: {type(score)}')

    return score


def split_str_parts_by(text: str, delimiters: List[str]):
    """Split the text field into parts.

    Args:
        text: A text to be split.
        delimiters: The delimiters.

    Returns:
        The split text in list of dicts.
    """
    all_start_chars = [d[0] for d in delimiters]
    all_length = [len(d) for d in delimiters]

    text_list = []
    last_words = ''

    while len(text) > 0:
        for char_idx, char in enumerate(text):
            match_index = [
                idx for idx, start_char in enumerate(all_start_chars)
                if start_char == char
            ]
            is_delimiter = False
            for index in match_index:
                if text[char_idx:char_idx
                        + all_length[index]] == delimiters[index]:
                    if last_words:
                        if text_list:
                            text_list[-1]['content'] = last_words
                        else:
                            text_list.append({
                                'key': '',
                                'content': last_words
                            })
                    last_words = ''
                    text_list.append({'key': delimiters[index]})
                    text = text[char_idx + all_length[index]:]
                    is_delimiter = True
                    break
            if not is_delimiter:
                last_words += char
            else:
                break
        if last_words == text:
            text = ''

    text_list[-1]['content'] = last_words
    return text_list


def split_parts_by_regex(text_list: list, regex_delimiters: Dict[str, List[float]]) -> None:
    import re
    compiled_patterns = [(re.compile(pattern), scale) for pattern, scale in regex_delimiters.items()]
    for i in range(len(text_list) - 1, -1, -1):
        item = text_list[i]
        if item.get('key') == '':
            res_text = item['content']
            last_idx = 0
            segments = []

            for pattern, scale in compiled_patterns:
                matches = list(re.finditer(pattern, res_text))
                for match in matches:
                    if match.start() > last_idx:
                        segments.append({'key': '', 'content': res_text[last_idx:match.start()]})
                    segments.append({'key': scale[0], 'content': match.group(0)})
                    last_idx = match.end()

            if last_idx < len(res_text):
                segments.insert(0, {'key': '', 'content': res_text[last_idx:]})

            if segments:
                text_list[i:i + 1] = segments


def calculate_loss_scale(query: str,
                         response: str,
                         use_loss_scale=False,
                         response_loss_scale_map: Optional[Dict[str, list]] = None,
                         query_loss_scale_map: Optional[Dict[str, list]] = None) -> Tuple[List[str], List[float]]:
    """Calculate the loss scale by splitting the agent response.

    This algorithm comes from paper: https://arxiv.org/pdf/2309.00986.pdf

    Agent response format:

    ```text
        Thought: you should always think about what to do
        Action: the action to take, should be one of the above tools[fire_recognition,
            fire_alert, call_police, call_fireman]
        Action Input: the input to the action
        Observation: the result of the action
        ... (this Thought/Action/Action Input/Observation can be repeated zero or more times)
        Thought: I now know the final answer
        Final Answer: the final answer to the original input question
    ```

    Args:
        response: The response text
        use_loss_scale: Use weighted loss. With this, some part of the loss will be enhanced to improve performance.

    Returns:
        A tuple of agent response parts and their weights.
    """
    if use_loss_scale:
        # query loss scale map
        if query_loss_scale_map is not None:
            for key in query_loss_scale_map.keys():
                if key in query:
                    if isinstance(query_loss_scale_map[key], (float, int)):
                        query_loss_scale_map[key] = [query_loss_scale_map[key]]
                    loss_scale_value = query_loss_scale_map[key][0]
                    return [response], [float(loss_scale_value)]
        delimiters = list(k for k in response_loss_scale_map.keys() if len(response_loss_scale_map[k]) == 2)
        agent_parts = split_str_parts_by(response, delimiters)
        regex_delimiters = {k: v for k, v in response_loss_scale_map.items() if len(v) == 1}
        if len(regex_delimiters):
            split_parts_by_regex(agent_parts, regex_delimiters)
        weights = []
        agent_content = []
        for c in agent_parts:
            if isinstance(c['key'], (float, int)):
                weights += [c['key']]
                agent_content.append(c['content'])
            else:
                if c['key'] in response_loss_scale_map:
                    weights += [response_loss_scale_map[c['key']][0]]
                    weights += [response_loss_scale_map[c['key']][1]]
                    agent_content.append(c['key'])
                    agent_content.append(c['content'])
                else:
                    weights += [1.0]
                    agent_content.append(c['content'])
        return agent_content, weights
    else:
        return [response], [1.0]


def get_bucket_sizes(max_length: int) -> List[int]:
    return [max_length // 4 * (i + 1) for i in range(4)]


def _get_closet_bucket(bucket_sizes, data_length):
    """Select the one from bucket_sizes that is closest in distance to
    data_length. This is required for TorchAcc.
    """
    cloest_length = sys.maxsize
    for b in bucket_sizes:
        if b == data_length or ((b < cloest_length) and (b > data_length)):
            cloest_length = b

    if cloest_length == sys.maxsize:
        bucket_sizes.append(data_length)
        cloest_length = data_length

    return cloest_length


def pad_and_split_batch(padding_to, input_ids, attention_mask, labels,
                        loss_scale, max_length, tokenizer, rank, world_size):
    if padding_to is None:
        longest_len = input_ids.shape[-1]
        bucket_sizes = get_bucket_sizes(max_length)
        bucket_data_length = _get_closet_bucket(bucket_sizes, longest_len)
        padding_length = bucket_data_length - input_ids.shape[1]
        input_ids = F.pad(input_ids, (0, padding_length), 'constant',
                          tokenizer.pad_token_id)
        attention_mask = F.pad(attention_mask, (0, padding_length), 'constant',
                               0)
        if loss_scale:
            loss_scale = F.pad(loss_scale, (0, padding_length), 'constant', 0.)
        labels = F.pad(labels, (0, padding_length), 'constant', -100)

    # manully split the batch to different DP rank.
    batch_size = input_ids.shape[0] // world_size
    if batch_size > 0:
        start = rank * batch_size
        end = (rank + 1) * batch_size
        input_ids = input_ids[start:end, :]
        attention_mask = attention_mask[start:end, :]
        labels = labels[start:end, :]
        if loss_scale:
            loss_scale = loss_scale[start:end, :]
    return input_ids, attention_mask, labels, loss_scale


def get_dist_setting() -> Tuple[int, int, int, int]:
    """return rank, local_rank, world_size, local_world_size"""
    rank = int(os.getenv('RANK', -1))
    local_rank = int(os.getenv('LOCAL_RANK', -1))
    world_size = int(os.getenv('WORLD_SIZE', 1))
    local_world_size = int(os.getenv('LOCAL_WORLD_SIZE', 1))
    return rank, local_rank, world_size, local_world_size


def use_torchacc() -> bool:
    return strtobool(os.getenv('USE_TORCHACC', '0'))


def fetch_one(element: Union[Tuple, List, Set, Dict, Any]) -> Any:
    if isinstance(element, (tuple, set, list)):
        for ele in element:
            out = fetch_one(ele)
            if out:
                return out
    elif isinstance(element, dict):
        return fetch_one(list(element.values()))
    else:
        return element
