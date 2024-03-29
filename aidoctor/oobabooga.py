#https://github.com/oobabooga/text-generation-webui/blob/main/docs/12%20-%20OpenAI%20API.md
#https://www.reddit.com/r/LocalLLaMA/comments/16vc45l/german_llms_based_on_llama2_pretraining_are/

import os
import requests
import json
from typing import List, Mapping, Optional, Any

from pydantic import Field
import sseclient
from langchain.llms.base import LLM

class Oobabooga(LLM):
    """
    A custom LLM class for Oobabooga Api
    
    Arguments:

    url: (str) The api url to use
    model_name: (str) The model name to use
    n_threads: (str) The number of threads to use
    n_predict: (str) The maximum numbers of tokens to generate
    temp: (str) Temperature to use for sampling
    top_p: (float) The top-p value to use for sampling
    top_k: (float) The top k values use for sampling
    n_batch: (int) Batch size for prompt processing
    repeat_last_n: (int) Last n number of tokens to penalize
    repeat_penalty: (float) The penalty to apply repeated tokens
    
    """
    url: str = Field(None, alias='url')
    model_name: str = Field(None, alias='model_name')

    temp:           Optional[float] = 0.7
    top_p:          Optional[float] = 0.1
    top_k:          Optional[int]   = 40
    n_batch:        Optional[int]   = 8
    n_threads:      Optional[int]   = 4
    n_predict:      Optional[int]   = 256
    max_tokens:     Optional[int]   = 200
    repeat_last_n:  Optional[int]   = 64
    repeat_penalty: Optional[float] = 1.18


    def __init__(self, url, model_name, **kwargs):
        super(Oobabooga, self).__init__()
        self.url = url
        self.model_name = model_name
    
    @property
    def _get_model_default_parameters(self):
        return {
            "max_tokens": self.max_tokens,
            "n_predict": self.n_predict,
            "top_k": self.top_k,
            "top_p": self.top_p,
            "temp": self.temp,
            "n_batch": self.n_batch,
            "repeat_penalty": self.repeat_penalty,
            "repeat_last_n": self.repeat_last_n,
        }

    @property
    def _identifying_params(self) -> Mapping[str, Any]:
        """
        Get all the identifying parameters
        """
        return {
            'model_name' : self.model_name,
            'model_parameters': self._get_model_default_parameters
        }

    @property
    def _llm_type(self) -> str:
        return 'oobabooga'
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None, *args, **kwargs) -> str:
        """
        Args:
            prompt: The prompt to pass into the model.
            stop: A list of strings to stop generation when encountered

        Returns:
            The string generated by the model        
        """
        
        url = "http://64.247.206.234:19695/v1/chat/completions"

        # The headers you want to send with the request
        headers = {
            "Content-Type": "application/json"
        }

        # The data you want to send with the request
        data = {
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "mode": "instruct",
            "instruction_template": "template1"
        }

        # Send a POST request
        response = requests.post(url, headers=headers, data=json.dumps(data))
        
        # Check for a successful response
        if response.status_code == 200:
            response_json = response.json()
            return response_json['choices'][0]['message']['content']
        else:
            # If the response was not successful, raise an error with the status code and message
            raise Exception(f"Error: {response.status_code} {response.reason} - {response.text}")