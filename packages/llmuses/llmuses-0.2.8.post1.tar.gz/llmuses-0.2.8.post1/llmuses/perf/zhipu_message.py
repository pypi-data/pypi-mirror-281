
from typing import Dict
import json

def get_query(model: str, prompt: str, **kwargs) -> Dict:
    """Get the query of from prompt and other parameters.

    Args:
        model (str): The model name.
        prompt (str): The input prompt.

    Returns:
        Dict: The request body.
    """
    messages = [{'role': 'user', 'content': prompt}]
    if prompt is None:
        raise Exception("Invalid parameters.")
    return {
        "model": model,
        "messages": messages,
        "stream": True,
        **kwargs
    }
    
def parse_responses(responses, **kwargs) -> Dict:
    """Parser responses and return number of request and response tokens.

    Args:
        responses (List[bytes]): List of http response body, for stream output,
            there are multiple responses, for general only one. 

    Returns:
        Dict: Return the prompt token and completion tokens.
    """
    last_response = responses[-1]
    js = json.loads(last_response)
    return js['usage']['prompt_tokens'], js['usage']['completion_tokens']