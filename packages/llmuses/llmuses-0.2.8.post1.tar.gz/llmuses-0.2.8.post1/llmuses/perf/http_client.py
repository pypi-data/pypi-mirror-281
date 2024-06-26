"""LLM performance benchmark client.
"""
import argparse
import asyncio
import json
import sqlite3, os
import time
import base64
import pickle
import importlib.util
import sys
from typing import List, Dict
from datetime import datetime, timezone
import aiohttp
from http import HTTPStatus
from server_sent_event import ServerSentEvent
import aiohttp
import numpy as np

from _logging import logger

_current_path = os.path.dirname(os.path.abspath(__file__))

_query_send_completed = False
_data_process_completed = False
_table_name = "result"   

async def on_request_start(session, context, params):
    logger.info(f'Starting request: <{params}>')

async def on_request_chunk_sent(session, context, params):
    logger.info(f'Request body: {params}')
    
async def on_response_chunk_received(session, context, params):
    logger.info(f'Response info: <{params}>')

class AioHttpClient:
    def __init__(self, 
                 url: str, 
                 conn_timeout: int = 120, 
                 read_timeout: int = 120,
                 headers: Dict = None,
                 debug: bool = False):
        # one client only has one connection
        client_timeout = aiohttp.ClientTimeout(total=read_timeout + conn_timeout,
                                               connect=conn_timeout,
                                               sock_read=read_timeout)
        if debug:
            trace_config = aiohttp.TraceConfig()
            trace_config.on_request_start.append(on_request_start)
            trace_config.on_request_chunk_sent.append(on_request_chunk_sent)
            # not support server sent event(stream=true)
            trace_config.on_response_chunk_received.append(on_response_chunk_received)
        self.client = aiohttp.ClientSession(trace_configs= [trace_config] if debug else [], 
                                            connector=aiohttp.TCPConnector(limit=1),
                                            timeout=client_timeout)
        ua = "modelscope_bench"
        self.headers = {"user-agent": ua}
        if headers:
            self.headers.update(headers)
        self.url = url

    async def __aenter__(self):
       pass

    async def __aexit__(self, exc_type, exc, tb):
        await self.client.close()

    async def aio_call(self):
        response = self._handle_request()
        if self.stream:
            return (item async for item in response)
        else:
            result = await response.__anext__()
            try:
                await response.__anext__()
            except StopAsyncIteration:
                pass
            return result

    async def _handle_stream(self, response):
        is_error = False
        status_code = response.status
        async for line in response.content:
            if line:
                line = line.decode("utf8")
                line = line.rstrip("\n").rstrip("\r")
                sse_msg = ServerSentEvent.decode(line)
                if not sse_msg:
                    continue
                if sse_msg.event and sse_msg.event == "error": # dashscope error
                    is_error = True

                if sse_msg.data:
                    if sse_msg.data.startswith("[DONE]"): # openai api completed
                        break
                    yield (is_error, status_code, sse_msg.data)
                    # yield data

    async def _handle_response(self, response: aiohttp.ClientResponse):
        if (response.status == HTTPStatus.OK and "text/event-stream" in response.content_type):
            async for is_error, status_code, data in self._handle_stream(response):
                yield (is_error, status_code, data)
        elif response.status == HTTPStatus.OK:
            content = await response.read()
            yield (False, HTTPStatus.OK, content)
        else:
            if "application/json" in response.content_type:
                error = await response.json()
                yield (True, response.status, error)
            else:
                msg = await response.read()
                yield (True, response.status, msg)

    async def post(self, body):
        try:
            headers = {"Content-Type": "application/json", **self.headers}
            response = await self.client.request("POST",
                                             url=self.url,
                                             json=body,
                                             headers=headers)
            async with response:
                async for rsp in self._handle_response(response):
                    yield rsp
        except aiohttp.ClientConnectorError as e:
            logger.error(e)
            raise e
        except Exception as e:
            logger.error(e)
            raise e

def dynamic_import_module(input_output_process_file_path: str):
    """Dynamic import input output process python file.

    Args:
        input_output_process_file_path (str): The absolute path of the 
            input output process python path, or name of the format, 
            system support openai, dashscope format.
    """
    module_name = 'input_output_process'

    input_output_spec = importlib.util.spec_from_file_location(module_name, input_output_process_file_path)
    input_output_process_module = importlib.util.module_from_spec(input_output_spec)
    sys.modules[module_name] = input_output_process_module
    input_output_spec.loader.exec_module(input_output_process_module)
    return input_output_process_module

def get_input_output_processor(input_output_format: str):
    if input_output_format in ['vllm_qwen_openai_completion', 'dashscope_message']:
        return dynamic_import_module(os.path.join(_current_path, '%s.py'%input_output_format))
    else:
        return dynamic_import_module(input_output_format)
        
async def dispatch_requests_worker(request_queue: asyncio.Queue, args):
    input_output_processor = get_input_output_processor(args.format)
    input_requests = []
    if args.prompt is not None:
        if args.prompt.startswith("@"): # read local as prompt, same as curl --data
            with open(args.prompt, 'r', encoding='utf-8') as f:
                prompt = f.read()
        else:
            prompt = args.prompt
        input_requests = [input_output_processor.get_query(model=args.model,
                                                prompt=prompt,
                                                **(args.parameters))]*args.number
    elif args.dataset is not None:
        input_prompts = []
        min_prompt_length = 0
        max_prompt_length = 1000000000
        if args.max_prompt_length is not None:
            max_prompt_length = args.max_prompt_length
        if args.min_prompt_length is not None:
            min_prompt_length = args.min_prompt_length
        if args.prompt_generator is not None:
            prompt_generator_module = dynamic_import_module(args.prompt_generator)
            for prompt in prompt_generator_module.prompt_generator(args.dataset):
                input_prompts.append(prompt)
        else: # default read file line by line
            with open(args.dataset, "r", encoding="UTF-8") as f:
                input_prompts = f.readlines()
        input_requests = []
        for prompt in input_prompts:
            prompt_length = len(prompt)
            if prompt_length > min_prompt_length and prompt_length < max_prompt_length:
                input_requests.append(input_output_processor.get_query(model=args.model,
                                                    prompt=prompt,
                                                    **(args.parameters)))
                if len(input_requests) >= args.number:
                    break
    if not input_requests:
        raise "Not input querys"

    total_query_counter = 0
    for request in input_requests:
        await request_queue.put(request)
        if args.rate == float("inf"):
            # If the request rate is infinity, then we don't need to wait.
            continue
        # Sample the request interval from the exponential distribution.
        interval = np.random.exponential(1.0 / args.rate)
        # The next request will be sent after the interval.
        await asyncio.sleep(interval)
        total_query_counter += 1
    return total_query_counter


class BenchmarkData(dict):
    """Benchmark info, two parts
    1. query info.
       prompt length
    2. response info
       start send time
       list of package_receive_time
           package info.
       response complete time
           total response info(response tokens)       
    """
    def __init__(self):
        pass 


def calculate_query_stream_metric(benchmark_data):
    first_chunk_latency = benchmark_data["chunk_times"][0] - benchmark_data["start_time"] # the first chunk latency
    n_chunks = len( benchmark_data["chunk_times"]) - 2 # minus first and last chunk.
    n_chunks_time = benchmark_data["chunk_times"][-2] - benchmark_data["chunk_times"][0] # -2 to last chunk
    return (first_chunk_latency, n_chunks, n_chunks_time)

async def statistic_benchmark_metric_worker(benchmark_data_queue: asyncio.Queue, args):
    """Statistics of performance metrics based on performance data
    """
    n_succeed_queries = 0
    n_failed_queries = 0
    total_first_chunk_latency = 0
    total_latency = 0.0
    n_total_chunks = 0
    n_total_prompt_tokens = 0
    n_total_completion_tokens = 0
    qps = 0
    concurrency = args.parallel
    start_time = None
    total_chunks_time = 0.0
    avg_latency = -1
    avg_first_chunk_latency = -1
    avg_token_per_seconds = -1
    avg_time_per_token = -1
    n_avg_chunks = -1
    avg_chunk_time = -1
    avg_prompt_tokens =-1
    avg_completion_tokens = -1
    total_time = 1 # avoid divide by zero
    n_total_queries = 0
    # avg generate tps generated tokens / time 
    # avg chunk time, first latency - avg_chunk_time == first latency, 去掉第一个和最后一个，第一个和prefill合并了，最后一个生成token可能比较短
    # avg prefill tps
    # prefill time = 首包时间-avg_chunk_time
    # n-tokens-per-trunk 
    n_benchmark_result = 0
    response_parser = get_input_output_processor(args.format)
    if args.result_file:
        result_db_path = args.result_file
    else:
        utc_dt = datetime.now(timezone.utc)
        current_time = utc_dt.astimezone().strftime("%Y_%m_%d_%H_%M_%S_%f")
        result_db_path = "./benchmark_%s.db"%current_time
    con = sqlite3.connect(result_db_path)
    
    db_cur = con.cursor()
    # create table      
    # TPS output tokens per second
    # tpot Time per ooutput token
    db_cur.execute("CREATE TABLE %s(request, start_time, chunk_times, success, \
                   response_messages, completed_time, latency, first_chunk_latency, \
                   n_chunks, chunk_time, prompt_tokens, completion_tokens)"%_table_name)
    if args.wandb_api_key is not None:
        import wandb
        name = args.wandb_name if args.wandb_name is not None else '%s_%s' % (args.model, current_time)
        wandb.init(
        project="perf_benchmark",   
        name=name,     
        # track run metadata
        config={
        "model": args.model,
        "time": current_time
        })
        os.environ["WANDB_SILENT"] = "true"
        
    while True:
        try:
            benchmark_data = benchmark_data_queue.get_nowait()                
            benchmark_data_queue.task_done()
            n_benchmark_result += 1
        except asyncio.QueueEmpty as e:
            if _data_process_completed:
                break
            await asyncio.sleep(1)
            continue
        if start_time is None:
            start_time = benchmark_data["start_time"] # start time with first request start time
        # total requests
        total_time = time.perf_counter() - start_time
        
        if benchmark_data["success"]:
            n_succeed_queries += 1
            n_query_trunks = len(benchmark_data["chunk_times"])
            query_latency = benchmark_data["completed_time"] - benchmark_data["start_time"]
            if n_query_trunks > 1:
                query_first_chunk_latency, query_n_chunks, query_n_chunks_time = calculate_query_stream_metric(benchmark_data)
            else:
                query_first_chunk_latency = query_latency     # not stream mode, query latency is equal total latency
                query_n_chunks = 1
                query_n_chunks_time = query_latency
            
            n_query_prompt_tokens, n_query_completion_tokens = response_parser.parse_responses(benchmark_data["response_messages"])
            n_total_prompt_tokens += n_query_prompt_tokens
            n_total_completion_tokens += n_query_completion_tokens
            
            total_first_chunk_latency += query_first_chunk_latency
            total_latency += query_latency
            n_total_chunks += query_n_chunks
            total_chunks_time += query_n_chunks_time

            # calc average
            avg_first_chunk_latency = total_first_chunk_latency / n_succeed_queries
            # average latency
            avg_latency = total_latency / n_succeed_queries
            # average generate chunks
            if n_query_trunks > 1:
                n_avg_chunks = n_total_chunks / n_succeed_queries + 2     # we remove the frist and last chunk.
            else:
                n_avg_chunks = n_total_chunks / n_succeed_queries
            avg_chunk_time = total_chunks_time / n_total_chunks            
            avg_prompt_tokens = n_total_prompt_tokens / n_succeed_queries
            avg_completion_tokens = n_total_completion_tokens / n_succeed_queries
            # avg generate tps generated tokens / time 
            avg_token_per_seconds = n_total_completion_tokens / total_time
            avg_time_per_token = total_time / n_total_completion_tokens
            # save the benchmark data to database.
            # save data to dist.
            insert_sql = "INSERT INTO %s VALUES('%s', %s, '%s', '%s', '%s', %s, %s, %s, %s, %s, %s, %s)" % (
                _table_name,
                base64.b64encode(pickle.dumps(benchmark_data["request"])).decode("ascii"), 
                benchmark_data["start_time"],
                json.dumps(benchmark_data["chunk_times"]),
                benchmark_data["success"],
                base64.b64encode(pickle.dumps(benchmark_data["response_messages"])).decode("ascii"),
                benchmark_data["completed_time"],
                query_latency,
                query_first_chunk_latency,
                query_n_chunks,
                query_n_chunks_time,
                n_query_prompt_tokens,
                n_query_completion_tokens
            )        
        else:
            n_failed_queries += 1
            # save the benchmark data to database.
            # save data to dist.
            insert_sql = "INSERT INTO %s(request, start_time, chunk_times, success, response_messages, completed_time)\
                VALUES('%s', %s, '%s', '%s', '%s', %s)" % (
                _table_name,
                base64.b64encode(pickle.dumps(benchmark_data["request"])).decode("ascii"), 
                benchmark_data["start_time"],
                json.dumps(benchmark_data["chunk_times"]),
                benchmark_data["success"],
                base64.b64encode(pickle.dumps(benchmark_data["response_messages"])).decode("ascii"),
                benchmark_data["completed_time"]
            )  
        n_total_queries = float(n_succeed_queries + n_failed_queries) # float for calc
        qps = n_total_queries / total_time
        db_cur.execute(insert_sql)
        con.commit()
        default_ndigits = 3
        message = {"Time": round(total_time, default_ndigits), 
                   "concurrency": concurrency,
                   "completed": int(n_total_queries), 
                   "succeed": n_succeed_queries, 
                   "failed": n_failed_queries, 
                   "qps": round(qps, default_ndigits), 
                   "latency": round(avg_latency, default_ndigits), 
                   "time to first token": round(avg_first_chunk_latency, default_ndigits), 
                   "throughput(output tokens per second)": round(avg_token_per_seconds, default_ndigits), 
                   "time per output token": round(avg_time_per_token, 5), 
                   "package per request": round(n_avg_chunks, default_ndigits), 
                   "time per package": round(avg_chunk_time, default_ndigits), 
                   "input tokens per request": round(avg_prompt_tokens, default_ndigits), 
                   "output tokens per request": round(avg_completion_tokens, default_ndigits)}
        if args.wandb_api_key is not None:
            wandb.log(message)
        if int(n_total_queries) % args.log_every_n_query == 0:
            msg = json.dumps(message)
            msg = msg[1:-1].replace('"', '')
            logger.info(msg)
    con.commit()
    con.close()
    return (total_time, n_total_queries, 
            n_succeed_queries, n_failed_queries, 
            qps, avg_latency, avg_first_chunk_latency, 
            n_avg_chunks, avg_chunk_time, 
            avg_prompt_tokens, avg_completion_tokens, 
            avg_token_per_seconds, avg_time_per_token, 
            result_db_path)

def summary_result(expected_number_of_queries,
                   total_time, 
                   n_total_queries, 
                   n_succeed_queries, 
                   n_failed_queries, 
                   qps, 
                   avg_latency, 
                   avg_first_chunk_latency, 
                   n_avg_chunks, 
                   avg_chunk_time, 
                   avg_prompt_tokens, 
                   avg_completion_tokens, 
                   avg_token_per_seconds, 
                   avg_time_per_token,
                   result_db_path, args):
    
    print("Benchmarking summary: ")
    print(" Time taken for tests: %.3f seconds" % total_time)
    print(" Expected number of requests: %s" % expected_number_of_queries)
    print(" Number of concurrency: %d" % args.parallel)
    print(" Total requests: %d" % n_total_queries)
    print(" Succeed requests: %d" % n_succeed_queries)
    print(" Failed requests: %d" % n_failed_queries)
    print(" Average QPS: %.3f" % qps)
    print(" Average latency: %.3f" % avg_latency)
    print(" Throughput(average output tokens per second): %.3f" % avg_token_per_seconds)
    print(" Average time to first token: %.3f" % avg_first_chunk_latency)
    print(" Average input tokens per request: %.3f" % avg_prompt_tokens)
    print(" Average output tokens per request: %.3f" % avg_completion_tokens)
    print(" Average time per output token: %.5f" % avg_time_per_token)
    print(" Average package per request: %.3f" % n_avg_chunks)
    print(" Average package latency: %.3f" % avg_chunk_time)
    
    con = sqlite3.connect(result_db_path)
    query_sql = "SELECT start_time, chunk_times, success, \
                   completed_time, latency, first_chunk_latency, \
                   n_chunks, chunk_time, prompt_tokens, completion_tokens \
                       FROM %s WHERE success='True' ORDER BY first_chunk_latency ASC"%_table_name
    
    percentiles = [50, 66, 75, 80, 90, 95, 98, 99]
    with con:
        rows = con.execute(query_sql).fetchall()
        if len(rows) > 0:
            print(" Percentile of time to first token: ")
            for percentile in percentiles:
                idx = (int)(n_total_queries*percentile/100)
                row = rows[idx]
                print("     p%s: %.4f"%(percentile, row[5] if row[5] is not None else float("inf")))
                #print(row)
            print(" Percentile of request latency: ")
            latency_index = 4
            rows.sort(key=lambda x: x[latency_index])
            for percentile in percentiles:
                idx = (int)(n_total_queries*percentile/100)
                row = rows[idx]
                print("     p%s: %.4f"%(percentile, row[latency_index] if row[latency_index] is not None else float("inf")))        
    con.close()

async def send_requests_worker(task_id, request_queue: asyncio.Queue, benchmark_data_queue: asyncio.Queue, args):    
    client = AioHttpClient(args.url,
                           conn_timeout=args.connect_timeout,
                           read_timeout=args.read_timeout, 
                           headers=args.headers,
                           debug=args.debug)
    async with client:
        while True:        
            # Get a request out of the queue.
            try:
                request = request_queue.get_nowait()
                request_queue.task_done()
            except asyncio.QueueEmpty as e:
                if _query_send_completed:
                    break
                await asyncio.sleep(0.01)
                continue    # keep polling querys
            benchmark_data = BenchmarkData()
            benchmark_data["request"] = request
            benchmark_data["start_time"] = time.perf_counter()
            benchmark_data["chunk_times"] = []
            benchmark_data["success"] = False
            collected_messages = []
            try:
                async for (is_error, state_code, response_data) in client.post(request):
                    if is_error or state_code != HTTPStatus.OK:
                        logger.error("Request: %s failed, state_code: %s, data: %s"%(request, state_code, response_data.decode('utf-8')))
                        break
                    else:
                        if response_data:
                            collected_messages.append(response_data)  # save the message
                            logger.debug(response_data)
                            benchmark_data["chunk_times"].append(time.perf_counter())
                
                benchmark_data["response_messages"] = collected_messages
                benchmark_data["completed_time"] = time.perf_counter()
                benchmark_data["success"] = not is_error
                await benchmark_data_queue.put(benchmark_data)
            except Exception as e:
                if response_data:
                    collected_messages.append(response_data)  # save the message
                benchmark_data["response_messages"] = collected_messages
                benchmark_data["completed_time"] = time.perf_counter()
                await benchmark_data_queue.put(benchmark_data)
                logger.error("Request query: %s exception, response: %s" % (request, response_data))
                logger.error(e)

async def benchmark(args) -> None:
    request_tasks: List[asyncio.Task] = []
    # Queues can be used to distribute workload between several concurrent tasks
    # Create a queue that we will use to store our "workload".
    request_queue = asyncio.Queue()
    benchmark_data_queue = asyncio.Queue()
    dispatch_task = asyncio.create_task(dispatch_requests_worker(request_queue, args))
    statistic_benchmark_metric_task = asyncio.create_task(statistic_benchmark_metric_worker(benchmark_data_queue, args))
    for idx, task in enumerate(range(args.parallel)):
        task = asyncio.create_task(send_requests_worker(idx, request_queue, benchmark_data_queue, args))
        request_tasks.append(task)
    
   
    expected_number_of_queries = await dispatch_task # wait for dispatch task complete
    await request_queue.join()
    global _query_send_completed   
    _query_send_completed = True
    await asyncio.gather(*request_tasks, return_exceptions=True)
    await benchmark_data_queue.join() # wait for all query is processed
    global _data_process_completed
    _data_process_completed = True
    (total_time, n_total_queries, 
     n_succeed_queries, n_failed_queries, 
     qps, avg_latency, 
     avg_first_chunk_latency, n_avg_chunks, 
     avg_chunk_time, avg_prompt_tokens, 
     avg_completion_tokens, avg_token_per_seconds, 
     avg_time_per_token, result_db_path) = await statistic_benchmark_metric_task

    summary_result(expected_number_of_queries, total_time, n_total_queries, n_succeed_queries, 
            n_failed_queries, qps, avg_latency, avg_first_chunk_latency, 
            n_avg_chunks, avg_chunk_time,
            avg_prompt_tokens, avg_completion_tokens, 
            avg_token_per_seconds, avg_time_per_token, 
            result_db_path, args)
    await asyncio.sleep(0.250)

# from: https://gist.github.com/vadimkantorov/37518ff88808af840884355c845049ea
class ParseKVAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for each in values:
            try:
                key, value = each.split("=")
                getattr(namespace, self.dest)[key] = value
            except ValueError as ex:
                message = "\nTraceback: {}".format(ex)
                message += "\nError on '{}' || It should be 'key=value'".format(
                    each)
                raise argparse.ArgumentError(self, str(message))

def main(args):
    asyncio.run(benchmark(args))
    
def add_argument(parser: argparse.ArgumentParser):
    parser.add_argument("--model", type=str, required=True, 
                        help="The test model name.")
    parser.add_argument("--url", type=str, default="localhost")
    parser.add_argument("--dataset", type=str, required=False,
                        help="Path to the dataset, with prompt line by line")
    parser.add_argument("--connect-timeout", type=int, default=120,
                        help="The network connection timeout")
    parser.add_argument("--read-timeout", type=int, default=120,
                        help="The network read timeout")
    parser.add_argument("--max-prompt-length", type=int, required=False,
                        help="Maximum input prompt length")
    parser.add_argument("--min-prompt-length", type=int, required=False,
                        help="Minimum input prompt length.")
    parser.add_argument("--prompt", type=str, required=False,
                         help="Specified the request prompt, all the query will use this prompt.")
    parser.add_argument("-n", "--number", type=int, default=1000,
                        help="How many requests to be made.")
    parser.add_argument("--parameters", nargs="+", 
                        dest="parameters",
                        default={},
                        action=ParseKVAction,
                        help="Extra parameters accepts by key1=value1 key2=value2. "
                             "The parameters will be use for each query." 
                             "You can use this parameter to specify sample parameters such as top_p, top_k ",
                        metavar="KEY1=VALUE1")
    parser.add_argument("--headers", nargs="+", dest="headers",
                        action=ParseKVAction,
                        help="Extra http headers accepts by key1=value1 key2=value2. "
                             "The headers will be use for each query." 
                             "You can use this parameter to specify http auchorization and other header.",
                        metavar="KEY1=VALUE1")
    parser.add_argument("--parallel", type=int, default=1,
                         help="Set number of concurrency request, default 1")
    parser.add_argument("--rate", type=int, default=None,
                         help="Number of requests per second. default None, if it set to -1,"
                             "then all the requests are sent at time 0. "
                             "Otherwise, we use Poisson process to synthesize "
                             "the request arrival times.  Mutual exclusion with parallel")
    parser.add_argument("--log-every-n-query", type=int, default=10, 
                        help="Logging every n query.")
    parser.add_argument("--n-tokens-per-trunk",
                        type=int,
                        default=16,
                        help="Number of tokens per stream output trunk")
    parser.add_argument("--format",
                        type=str,
                        default="vllm_qwen_openai_completion",
                        help="Specify the request/response format, current support,"
                             "[vllm_qwen_openai_completion, dashscope_message], "
                             "you can define your input output format via python file,"
                             "please ref the vllm_qwen_openai_completion.py")
    parser.add_argument("--prompt-generator", type=str, default=None,
                        help="Specify the prompt generator python file, default \
                            we will read data line by line and prompt is one line")
    parser.add_argument("--result-file", type=str,
                        help="The path of the result file, default file in current directory name with current_time")
    parser.add_argument("--wandb-api-key", type=str, default=None,
                        help="The wandb api key, if set the metric will be saved to wandb.")
    parser.add_argument("--wandb-name", type=str, 
                        help="The one db result name, default: {model_name}_{current_time}")
    parser.add_argument("--debug", action='store_true', default=False,
                        help='Debug request send.')
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Benchmark large language model server performance.")
    add_argument(parser)
    args = parser.parse_args()
    main(args)

