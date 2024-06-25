# -*- coding: utf-8 -*-
# Copyright (c) Louis Brulé Naudet. All Rights Reserved.
# This software may be used and distributed according to the terms of License Agreement.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import asyncio
import json
import logging
import requests

import httpx

from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Type,
    Tuple,
    Union,
    Mapping,
    TypeVar,
    Callable,
    Optional,
    Sequence,
)

from gspl._decorators import retry

# Set up logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class Retriever:
    """
    A class for retrieving completions from an API client.

    This class provides methods for generating text completions using an API client,
    either synchronously or asynchronously.

    Attributes
    ----------
    api_key : str
        The API key for authenticating requests.

    headers : dict
        Headers to be included in the API request.

    Methods
    -------
    completion(payload)
        Generate a completion using the API.

    async_completion(payload)
        Asynchronously completes a chat conversation using the API.
    """
    def __init__(
        self, 
        api_key: str, 
        headers: Optional[dict] = None
    ):
        """
        Initialize the Retriever with an API key, API URL, and optional headers.

        Parameters
        ----------
        api_key : str
            The API key for authenticating requests.

        headers : dict, optional
            Headers to be included in the API request (default is None, which sets the Authorization header using the provided api_key).
        """
        self.api_key: str = api_key
        self.headers: dict = headers if headers else {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }


    def completion(
        self, 
        payload: dict,
        api_url: Optional[str] = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B", 
        validate_payload: Optional[str] = False
    ) -> dict:
        """
        Generate a completion using the API.

        Parameters
        ----------
        payload : dict
            A dictionary containing the input and optional parameters for the API call.
            - top_k : int, optional
                Define the top tokens considered within the sample operation to create new text.
            - top_p : float, optional
                Define the tokens that are within the sample operation of text generation.
            - temperature : float, optional
                The temperature of the sampling operation (default is 1.0).
            - repetition_penalty : float, optional
                The penalty for repeating tokens (default is None).
            - max_new_tokens : int, optional
                The amount of new tokens to be generated (default is None).
            - max_time : float, optional
                The maximum time in seconds for the query (default is None).
            - return_full_text : bool, optional
                Whether to return the full text including the input (default is True).
            - num_return_sequences : int, optional
                The number of propositions to return (default is 1).
            - do_sample : bool, optional
                Whether to use sampling (default is True).
            - options : dict, optional
                A dictionary containing additional options:
                    - use_cache : bool, optional
                        Whether to use caching (default is True).
                    - wait_for_model : bool, optional
                        Whether to wait for the model if not ready (default is False).

            Example structure:
            {
                "inputs": "Your input string here",
                "parameters": {
                    "top_k": int, optional,
                    "top_p": float, optional,
                    "temperature": float, optional (default is 1.0),
                    "repetition_penalty": float, optional,
                    "max_new_tokens": int, optional,
                    "max_time": float, optional,
                    "return_full_text": bool, optional (default is True),
                    "num_return_sequences": int, optional (default is 1),
                    "do_sample": bool, optional (default is True),
                    "options": {
                        "use_cache": bool, optional (default is True),
                        "wait_for_model": bool, optional (default is False)
                    }
                }
            }
        
        api_url : str, optional
            The URL endpoint of the API (default is "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B").

        validate_payload : str, optional
            A string indicating whether to validate the payload or not. 
            If set to True, the payload will be validated. 
            If set to False (default), the payload will not be validated.

        Returns
        -------
        dict
            A dictionary containing the generated completion data.

        Raises
        ------
        ValueError
            If the payload or its components have invalid types.

        requests.HTTPError
            If the API request returns an error status code.

        requests.RequestException
            If there is an error making the API request.
        """
        try:
            if validate_payload:
                self._validate_payload(
                    payload=payload
                )

            response = requests.post(
                api_url, 
                headers=self.headers, 
                json=payload
            )

            response.raise_for_status()  # Raise an exception for HTTP errors

            return json.loads(
                response.json()[0]["generated_text"]
            )

        except ValueError as ve:
            raise ve

        except requests.exceptions.HTTPError as http_err:
            raise requests.HTTPError(
                f"HTTP error occurred: {http_err}"
            )

        except requests.exceptions.RequestException as req_err:
            raise requests.RequestException(
                f"Request error occurred: {req_err}"
            )


    @retry(show_error=True)
    async def async_completion(
        self, 
        payload: dict,
        api_url: Optional[str] = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B", 
        validate_payload: Optional[str] = False
    ) -> dict:
        """
        Asynchronously completes a chat conversation using the API.

        Parameters
        ----------
        payload : dict
            A dictionary containing the input and optional parameters for the API call.
            - top_k : int, optional
                Define the top tokens considered within the sample operation to create new text.
            - top_p : float, optional
                Define the tokens that are within the sample operation of text generation.
            - temperature : float, optional
                The temperature of the sampling operation (default is 1.0).
            - repetition_penalty : float, optional
                The penalty for repeating tokens (default is None).
            - max_new_tokens : int, optional
                The amount of new tokens to be generated (default is None).
            - max_time : float, optional
                The maximum time in seconds for the query (default is None).
            - return_full_text : bool, optional
                Whether to return the full text including the input (default is True).
            - num_return_sequences : int, optional
                The number of propositions to return (default is 1).
            - do_sample : bool, optional
                Whether to use sampling (default is True).
            - options : dict, optional
                A dictionary containing additional options:
                    - use_cache : bool, optional
                        Whether to use caching (default is True).
                    - wait_for_model : bool, optional
                        Whether to wait for the model if not ready (default is False).

            Example structure:
            {
                "inputs": "Your input string here",
                "parameters": {
                    "top_k": int, optional,
                    "top_p": float, optional,
                    "temperature": float, optional (default is 1.0),
                    "repetition_penalty": float, optional,
                    "max_new_tokens": int, optional,
                    "max_time": float, optional,
                    "return_full_text": bool, optional (default is True),
                    "num_return_sequences": int, optional (default is 1),
                    "do_sample": bool, optional (default is True),
                    "options": {
                        "use_cache": bool, optional (default is True),
                        "wait_for_model": bool, optional (default is False)
                    }
                }
            }

        api_url : str, optional
            The URL endpoint of the API (default is "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B").

        validate_payload : str, optional
            A string indicating whether to validate the payload or not. 
            If set to True, the payload will be validated. 
            If set to False (default), the payload will not be validated.

        Returns
        -------
        dict
            A dictionary containing the generated completion data.

        Raises
        ------
        ValueError
            If the payload or its components have invalid types.

        httpx.HTTPStatusError
            If the API request returns an error status code.

        httpx.RequestError
            If there is an error making the API request.
        """
        try:
            if validate_payload:
                self._validate_payload(payload)

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    api_url, 
                    headers=self.headers, 
                    json=payload
                )

                response.raise_for_status()  # Raise an exception for HTTP errors
                
                return response.json()

        except ValueError as ve:
            raise ve

        except httpx.HTTPStatusError as http_err:
            raise httpx.HTTPStatusError(
                f"HTTP error occurred: {http_err}"
            )

        except httpx.RequestError as req_err:
            raise httpx.RequestError(
                f"Request error occurred: {req_err}"
            )


    def _validate_payload(
        self, 
        payload: dict
    ):
        """
        Validates the payload structure and types for API requests.

        Parameters
        ----------
        payload : dict
            A dictionary containing the input and optional parameters for the API call.

        Raises
        ------
        ValueError
            If the payload or its components have invalid types.
        """
        if not isinstance(payload, dict):
            raise ValueError("Payload must be a dictionary.")

        if "inputs" not in payload or not isinstance(payload["inputs"], str):
            raise ValueError("Payload must contain 'inputs' as a string.")

        parameters: dict = payload.get("parameters", {})

        if not isinstance(parameters, dict):
            raise ValueError("'parameters' must be a dictionary.")

        valid_types: dict = {
            "top_k": (int, type(None)),
            "top_p": (float, type(None)),
            "temperature": (float,),
            "repetition_penalty": (float, type(None)),
            "max_new_tokens": (int, type(None)),
            "max_time": (float, type(None)),
            "return_full_text": bool,
            "num_return_sequences": int,
            "do_sample": bool,
            "options": dict,
        }

        for key, types in valid_types.items():
            if key in parameters and not isinstance(parameters[key], types):
                raise ValueError(
                    f"'{key}' in 'parameters' must be {' or '.join(t.__name__ for t in types)}."
                )

        options: dict = parameters.get("options", {})

        if not isinstance(options, dict):
            raise ValueError("'options' within 'parameters' must be a dictionary.")

        valid_option_types: dict = {
            "use_cache": bool,
            "wait_for_model": bool,
        }

        for key, types in valid_option_types.items():
            if key in options and not isinstance(options[key], types):
                raise ValueError(
                    f"'{key}' in 'options' must be {types.__name__}."
                )