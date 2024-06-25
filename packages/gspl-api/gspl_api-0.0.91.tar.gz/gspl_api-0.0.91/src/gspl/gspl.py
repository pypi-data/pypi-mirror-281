# -*- coding: utf-8 -*-
# Copyright (c) Louis Brulé Naudet. All Rights Reserved.
# This software may be used and distributed according to the terms of License Agreement.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import concurrent.futures
import json
import logging
import os
import random
import re
import uuid

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

import langdetect
from datasets import (
    concatenate_datasets, 
    Dataset, 
    load_dataset
)
from dotenv import load_dotenv
from tqdm import tqdm

from gspl._chunks import TextSplitter
from gspl._decorators import retry, rate_limit
from gspl._retrieval import Retriever
from gspl._tokenizer import Token

# Set up logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)

load_dotenv()


class GSPL:
    """
    Gen-Selective Pseudo Labeler (GSPL)

    A class to generate multiple queries about a single document and apply a selection
    process using transformers. This class leverages large language models (LLMs) as a 
    judge technique to process datasets.

    The GSPL class provides methods to apply chat templates, label datasets, select outputs,
    and save processed datasets to Parquet files. It uses a completion client to generate
    responses based on provided prompts.

    Attributes
    ----------
    api_key : str
        API key for the completion client.

    client : Retriever
        A completion client initialized with the API key.

    dataset : Dataset
        The dataset to be processed.

    split : str
        The dataset split to be used (default is "train").

    rpm : int
        Requests per minute rate limit (default is 30).

    Methods
    -------
    __call__(column, completion_system_prompt, selection_system_prompt, payload, save_to, api_url='https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct', response_key='query', validate_payload=False)
        Executes the complete processing pipeline.

    chat_template(system_prompt, query)
        Creates a formatted chat template string from given system and user prompts.

    apply_chat_template(column, system_prompt, output='inputs')
        Apply a chat template to a dataset in parallel using multiple processes.

    completion(payload, api_url='https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct', response_key='query', validate_payload=False)
        Generates a completion response from the API.

    label(payload, api_url='https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct', inputs_column='inputs', response_key='query', output='queries', num_return_sequences=3, token_threshold=600, validate_payload=False)
        Labels the dataset using the completion client.

    select(payload, api_url='https://api-inference.huggingface.co/models/microsoft/Phi-3-medium-4k-instruct', inputs_column='inputs', response_key='query', output='query', validate_payload=False)
        Selects outputs from the labeled dataset.

    to_parquet(filepath)
        Saves the labeled dataset to a Parquet file.

    _apply_chat_template_parallel(row, column, system_prompt, output='inputs')
        Apply a chat template to a single row of a dataset.

    _load_dataset(dataset, split='train', streaming=False)
        Helper function to load a single dataset.

    _add_space_before_question_mark(string)
        Adds a space before each question mark in a string if not already present.
    """
    def __init__(
        self, 
        api_key: str,
        dataset: Dataset,
        split: Optional[str] = "train",
        streaming: Optional[bool] = False,
        rpm: Optional[int] = 30,
    ) -> None:
        """
        Initializes the GSPL class with a completion client.

        Parameters
        ----------
        api_key : str
            API key for the completion client.
        
        dataset : Dataset
            The dataset to be processed.
        
        split : str, optional
            The dataset split to be used (default is "train").
        
        streaming : bool, optional
            Whether to stream the dataset (default is False).
        
        rpm : int, optional
            Requests per minute rate limit (default is 30).
        """
        self.api_key: str = api_key
        self.client: Retriever = Retriever(
            api_key=self.api_key
        )
        self.dataset: Dataset = self._load_dataset(
            dataset=dataset,
            split=split,
            streaming=streaming
        ) if isinstance(dataset, str) else dataset
        self.split: str = split
        self.rpm: int = rpm


    @staticmethod
    def chat_template(
        template: str, 
        **kwargs
    ) -> str:
        """
        Creates a formatted string using the provided template and keyword arguments.

        Parameters
        ----------
        template : str
            The template string to format.

        **kwargs : dict
            Keyword arguments to be used in the template string.

        Returns
        -------
        str
            A formatted string.
        
        Examples
        --------
        >>> template = "Hello, {name}! Welcome to {language}."
        >>> GSPL.chat_template(template, name="Bob", language="Python")
        '<|begin_of_text|><|start_header_id|>system<|end_header_id|>
        {system_prompt}<|eot_id|><|start_header_id|>user<|end_header_id|>
        {query}<|eot_id|><|start_header_id|>assistant<|end_header_id|>'
        """
        return template.format(**kwargs)


    def apply_chat_template(
        self, 
        template: str,
        output: Optional[str] = "inputs",
        **kwargs_columns
    ):
        """
        Apply a chat template to a dataset in parallel using multiple processes.

        Parameters
        ----------
        self : object
            The object containing the dataset.

        template : str
            The template to use for formatting the chat messages.

        output : str, optional
            The name of the column where the processed template will be saved.
            Default is "inputs"

        **kwargs_columns : dict
            Mapping of template placeholder names to dataset column names.

        Returns
        -------
        Dataset
            The dataset is updated in-place with the chat template applied.

        Examples
        --------
        >>> from datasets import load_dataset
        >>> dataset = load_dataset("json", data_files="path/to/data.json", field="data")
        >>> instance = GSPL(dataset)
        >>> instance.apply_chat_template('Hello, {name}! Welcome to {location}.', name='name', location='location')
        Applying chat template to dataset: 100%|██████████| 2/2 [00:00<00:00, 200.00it/s]
        >>> print(instance.dataset)
        Dataset({
            features: ['query', 'inputs'],
            num_rows: 2
        })
        ------------------------
        {'query': 'What is the capital of France?', 'inputs': 'Hello, Alice! Welcome to France.'}
        {'query': 'How old is the Earth?', 'inputs': 'Hello, Bob! Welcome to Earth.'}
        """
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_to_row = {
                executor.submit(
                    self._apply_chat_template_parallel, 
                    row, 
                    template,
                    output,
                    **kwargs_columns
                ): row for row in self.dataset
            }

            results = []

            for future in tqdm(
                concurrent.futures.as_completed(future_to_row), 
                total=len(self.dataset), 
                desc=f"Applying chat template to dataset"
            ):
                row = future_to_row[future]

                try:
                    processed_row = future.result()
                    results.append(processed_row)

                except Exception as exc:
                    logging.error(f"Error processing row: {row}, {exc}")

        self.dataset = Dataset.from_list(results)

        return self.dataset
        

    @rate_limit(rpm=30)
    # @retry(show_error=True)
    def completion(
        self,
        payload: dict,
        api_url: Optional[str] = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B",
        response_key: Optional[str] = "query",
        validate_payload: bool = False
    ) -> str:
        """
        Generates a completion response from the API.

        Parameters
        ----------
        payload : dict
            The payload to be sent to the completion API.

        api_url : str, optional
            The API URL for the completion client 
            (default is "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B").
        
        response_key : str, optional
            The key to extract the response from the completion client (default is "query").
        
        validate_payload : bool, optional
            Whether to validate the payload before sending (default is False).

        Returns
        -------
        str
            The completion response from the API.

        Examples
        --------
        >>> payload = {"inputs": "What is the capital of France?"}
        >>> instance = GSPL(api_key="your_api_key", dataset=dataset)
        >>> response = instance.completion(payload)
        >>> print(response)
        "The capital of France is Paris."
        """
        if "api-inference.huggingface.co" in api_url:
            response = self.client.completion(
                    payload=payload,
                    api_url=api_url, 
                    validate_payload=validate_payload
                )[response_key]

            if langdetect.detect(response) == "fr":
                response = self._add_space_before_question_mark(
                    string=response
                )

        return response


    def label(
        self,
        payload: dict,
        api_url: Optional[str] = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B",
        inputs_column: Optional[str] = "inputs",
        response_key: Optional[str] = "query",
        output: Optional[str] = "queries",
        num_return_sequences: Optional[int] = 2,
        token_threshold: Optional[int] = 600,
        validate_payload: bool = False,
    ) -> Dataset:
        """
        Labels the dataset using the completion client.

        This method generates multiple response sequences for each input and stores them
        in the output column.

        Parameters
        ----------
        payload : dict
            The payload to be sent to the completion API.
        
        api_url : str, optional
            The API URL for the completion client 
            (default is "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B").
        
        inputs_column : str, optional
            The name of the column containing the input text (default is "inputs").
        
        response_key : str, optional
            The key to extract the response from the completion client (default is "query").
        
        output : str, optional
            The name of the column to store the output (default is "queries").
        
        num_return_sequences : int, optional
            The number of response sequences to generate for each input (default is 3).
        
        token_threshold : int, optional
            The token threshold for the completion response (default is 600).
        
        validate_payload : bool, optional
            Whether to validate the payload before sending (default is False).

        Returns
        -------
        Dataset
            The labeled dataset.

        Examples
        --------
        >>> payload = {"inputs": "What is the capital of France?"}
        >>> instance = GSPL(api_key="your_api_key", dataset=dataset)
        >>> labeled_dataset = instance.label(payload)
        >>> print(labeled_dataset)
        Dataset({
            features: ['inputs', 'queries'],
            num_rows: 2
        })
        """
        results: list = []

        if inputs_column in self.dataset.features:
            for row in tqdm(self.dataset, desc=f"Processing dataset"):
                payload["inputs"] = row[inputs_column]

                try:
                    row[output] = list(
                        filter(
                            lambda query: query is not None,
                            [
                                self.completion(
                                    payload=payload,
                                    api_url=api_url,
                                    response_key=response_key,
                                    validate_payload=validate_payload
                                ) for i in tqdm(range(num_return_sequences))
                            ]
                        )
                    )

                    results.append(
                        row
                    )

                except Exception as exc:
                    logging.error(f"Error labeling row: {row}, {exc}")
                    continue

            self.dataset: Dataset = Dataset.from_list(
                mapping=results
            )

            print(self.dataset)
    
            return self.dataset


    def select(
        self,
        payload: dict,
        api_url: Optional[str] = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B",
        inputs_column: Optional[str] = "inputs",
        response_key: Optional[str] = "query",
        output: Optional[str] = "query",
        validate_payload: bool = False,
    ):
        """
        Selects outputs from the labeled dataset.

        Parameters
        ----------
        payload : dict
            The payload to be sent to the completion API.
        
        api_url : str, optional
            The API URL for the completion client 
            (default is "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B").
        
        inputs_column : str, optional
            The name of the column containing the input text (default is "inputs").
        
        response_key : str, optional
            The key to extract the response from the completion client (default is "query").
        
        output : str, optional
            The name of the column to store the output (default is "query").
        
        validate_payload : bool, optional
            Whether to validate the payload before sending (default is False).

        Returns
        -------
        Dataset
            The labeled dataset.

        Examples
        --------
        >>> payload = {"inputs": "What is the capital of France?"}
        >>> instance = GSPL(api_key="your_api_key", dataset=dataset)
        >>> instance.select(payload)
        >>> print(instance.dataset)
        Dataset({
            features: ['inputs', 'query'],
            num_rows: 2
        })
        """
        results: list = []

        if inputs_column in self.dataset.features:
            for row in tqdm(self.dataset, desc=f"Processing dataset"):
                payload["inputs"] = str(row[inputs_column])

                try:    
                    row[output] = self.completion(
                        payload=payload,
                        api_url=api_url,
                        response_key=response_key,
                        validate_payload=validate_payload
                    )

                    results.append(
                        row
                    )

                    print(row[output])

                except Exception as exc:
                    logging.error(f"Error labeling row: {row}, {exc}")
                    continue

            self.dataset: Dataset = Dataset.from_list(
                mapping=results
            )
    
            return self.dataset
            

    def to_parquet(
        self,
        filepath:str
    ):
        """
        Saves the labeled dataset to a Parquet file.

        Parameters
        ----------
        filepath : str
            The file path to save the labeled dataset.

        Returns
        -------
        None

        Examples
        --------
        >>> instance = GSPL(api_key="your_api_key", dataset=dataset)
        >>> instance.to_parquet("path/to/output.parquet")
        """
        self.dataset.to_parquet(
            filepath
        )

        return None


    def _apply_chat_template_parallel(
        self,
        row: dict, 
        template: str,
        output: Optional[str] = "inputs",
        **kwargs_columns
    ) -> dict:
        """
        Apply a chat template to a single row of a dataset.

        Parameters
        ----------
        row : dict
            A single row of the dataset.

        template : str
            The template to use for formatting the chat messages.

        output : str, optional
            The name of the column where the processed template will be saved.
            Default is "inputs"

        **kwargs_columns : dict
            Mapping of template placeholder names to dataset column names.

        Returns
        -------
        dict
            The updated row with the chat template applied.
        """
        kwargs = {
            key: row[column] for key, column in kwargs_columns.items()
        }

        row[output] = GSPL.chat_template(
            template, 
            **kwargs
        )

        return row


    def _load_dataset(
        self,
        dataset: str,
        split: Optional[str] = "train",
        streaming: Optional[bool] = False
    ) -> Dataset:
        """
        Helper function to load a single dataset.

        Parameters
        ----------
        dataset : str
            Name of the dataset to be loaded.
        
        split : str, optional
            Name of the split to load from the dataset (default is "train").
        
        streaming : bool, optional
            Whether to stream the dataset (default is False).

        Returns
        -------
        Dataset
            Loaded dataset object.

        Raises
        ------
        Exception
            If an error occurs during dataset loading.

        Examples
        --------
        >>> instance = GSPL(api_key="your_api_key", dataset="my_dataset")
        >>> loaded_dataset = instance._load_dataset("my_dataset", split="validation")
        >>> print(loaded_dataset)
        Dataset({
            features: ['feature1', 'feature2'],
            num_rows: 1000
        })
        """
        try:
            return load_dataset(
                dataset,
                split=split,
                streaming=streaming
            )

        except Exception as exc:
            logging.error(f"Error loading dataset {dataset}: {exc}")

            return None


    @staticmethod
    def _add_space_before_question_mark(
        string: str
    ) -> str:
        """
        Adds a space before each question mark in a string if not already present.

        Parameters
        ----------
        string : str
            The input string.

        Returns
        -------
        str
            The string with spaces added before question marks.

        Examples
        --------
        >>> text = "What is your name?How are you?"
        >>> GSPL._add_space_before_question_mark(text)
        'What is your name ?How are you ?'
        """
        return re.sub(
            r'(?<!\s)\?', " ?", string
        )