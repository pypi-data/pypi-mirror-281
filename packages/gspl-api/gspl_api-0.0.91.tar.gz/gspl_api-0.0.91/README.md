# GSPL: Gen-Selective Pseudo Labeling
[![Python](https://img.shields.io/pypi/pyversions/tensorflow.svg)](https://badge.fury.io/py/tensorflow) [![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0) ![Maintainer](https://img.shields.io/badge/maintainer-@louisbrulenaudet-blue)

## Introduction
![Plot](https://github.com/louisbrulenaudet/gspl/blob/main/thumbnail.png?raw=true)
The Gen-Selective Pseudo Labeler (GSPL) is a tool designed to generate multiple queries about the same document and apply selection techniques using transformers. It leverages large language models (LLMs) to function as a judge, enhancing the labeling process through advanced completion and selection methods. This project is particularly useful in scenarios where multi-query generation and selection are required to improve the quality and relevance of labeled data.

## Features

- **Multi-query Generation**: Generate multiple queries for a single document using powerful LLMs.
- **Selective Labeling**: Apply selection techniques to choose the best query from the generated set.
- **Parallel Processing**: Utilize multi-threading to efficiently process large datasets.
- **Integration with Hugging Face Transformers**: Seamlessly connect with transformer models hosted on Hugging Face.
- **Customizable Templates**: Apply custom chat templates to format queries and responses.

## Requirements

To use GSPL, you need the following dependencies installed:

- Python 3.7+
- Datasets
- tqdm
- langdetect
- tiktoken
- python-dotenv
- concurrent.futures

You can install the required dependencies using the following command:

```bash
pip install datasets tqdm langdetect python-dotenv tiktoken
```
Or using PyPI:

```bash
pip install gspl-api
```

## Installation

To install GSPL, clone the repository and navigate to the project directory:

```bash
git clone https://github.com/louisbrulenaudet/gspl.git
```
## Usage

### Initialization

To initialize the GSPL class, provide the API key, dataset, and optional parameters for dataset split, streaming, and rate limits.
```python
from gspl import GSPL

api_key = "your_api_key"
dataset = "your_dataset"

gspl_instance = GSPL(api_key=api_key, dataset=dataset)
```
### Methods

#### `__init__(self, api_key: str, dataset: Dataset, split: Optional[str] = "train", streaming: Optional[bool] = False, rpm: Optional[int] = 30) -> None`

Initializes the GSPL class with the specified parameters.

-   **Parameters**:
    -   `api_key`  (str): API key for the completion client.
    -   `dataset`  (Dataset): The dataset to be labeled.
    -   `split`  (str, optional): The dataset split to be used (default is "train").
    -   `streaming`  (bool, optional): Whether to stream the dataset (default is False).
    -   `rpm`  (int, optional): Requests per minute limit for rate limiting (default is 30).

#### `__call__(self, column: str, completion_system_prompt, selection_system_prompt, payload: dict, save_to: str, api_url: Optional[str] = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct", response_key: Optional[str] = "query", validate_payload: Optional[bool] = False)`

Executes the labeling process by applying chat templates, generating completions, and selecting the best responses.

-   **Parameters**:
    -   `column`  (str): Column name containing the query text.
    -   `completion_system_prompt`  (str): System prompt for generating completions.
    -   `selection_system_prompt`  (str): System prompt for selecting the best responses.
    -   `payload`  (dict): Payload to be sent to the completion API.
    -   `save_to`  (str): File path to save the labeled dataset.
    -   `api_url`  (str, optional): API URL for the completion client (default is "[https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct](https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct)").
    -   `response_key`  (str, optional): Key to extract the response from the completion client (default is "query").
    -   `validate_payload`  (bool, optional): Whether to validate the payload before sending (default is False).

#### Example Usage

```python
from gspl import GSPL

completion_template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>You are an AI assistant specialized in creating targeted questions for documents to build a domain-specific dataset for embedding model training. Your task is to:

    1. Analyze the given document or text.
    2. Generate a highly specific question that directly relates to the main content or key information in the document.
    3. Ensure the question is tailored to retrieve the document's content when used as a search query.
    4. Format the question as a JSON object with a single "query" key.
    5. Provide only the JSON object as output, without any additional text, introductions, or conclusions.

    Remember:
    - The question should be precise and relevant to the document's core information.
    - Avoid generic questions; focus on unique aspects of the given text.
    - Ensure the JSON is valid and can be parsed in Python.
    - Do not include any explanations or additional text outside the JSON object.<|eot_id|><|start_header_id|>user<|end_header_id|>
    {document}<|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """

selection_template = """<|begin_of_text|><|start_header_id|>system<|end_header_id|>You are an AI assistant specialized in selecting the most appropriate question from a batch of queries to match specific content. Your task is to:

    1. Analyze the given content or document.
    2. Review the provided batch of queries.
    3. Select the question that best relates to the main content or key information in the document.
    4. Ensure the selected question is highly specific and tailored to retrieve the document's content when used as a search query.
    5. Format the selected question as a JSON object with a single "best_query" key.
    6. Provide only the JSON object as output, without any additional text, introductions, or conclusions.

    Remember:
    - The selected question should be the most precise and relevant to the document's core information.
    - Prioritize questions that focus on unique aspects of the given text.
    - Ensure the JSON is valid and can be parsed in Python.
    - Do not include any explanations or additional text outside the JSON object.<|eot_id|><|start_header_id|>user<|end_header_id|>
    {queries}
    Source text : {document}
    <|eot_id|><|start_header_id|>assistant<|end_header_id|>
    """

payload = {
    "parameters": {
        "temperature": 0.9,
        "return_full_text": False,
        "max_new_tokens": 250,
        "do_sample": True,
        "top_k": 50,
        "top_p": 0.95
    },
    "options": {
        "use_cache": False,
        "wait_for_model": True
    }
}

gspl = GSPL(
    api_key="api_key",
    dataset=dataset["datasetId"],
    split="train"
)

gspl.apply_chat_template(
    template=completion_template,
    output="inputs",
    document="output",
)

gspl.label(
    payload=payload,
    output="queries"
)

gspl.apply_chat_template(
    template=selection_template,
    output="inputs",
    queries="queries",
    document="output"
)

gspl.select(
    payload=payload,
)

gspl.to_parquet(
    filepath=output_file
)
```
## Methods Explained

### `apply_chat_template(self, column: str, system_prompt: str, output: Optional[str] = "inputs") -> None`

Applies a chat template to a dataset in parallel using multiple processes.

-   **Parameters**:
    -   `template`  (str): The template prompt to use for the chat template.
    -   `output`  (str, optional): The name of the column where the processed template will be saved (default is "inputs").
    -   `**kwargs_columns`   (str): Mapping of template placeholder names to dataset column names.
-   **Returns**:
    -   `self.dataset`  (Dataset): The dataset is updated in-place with the chat template applied.

### `completion(self, payload: dict, api_url: Optional[str] = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct", response_key: Optional[str] = "query", validate_payload: bool = False) -> str`

Generates a completion response using the completion client.

-   **Parameters**:
    -   `payload`  (dict): The payload to be sent to the completion API.
    -   `api_url`  (str, optional): The API URL for the completion client (default is "[https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct](https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct)").
    -   `response_key`  (str, optional): The key to extract the response from the completion client (default is "query").
    -   `validate_payload`  (bool, optional): Whether to validate the payload before sending (default is False).
-   **Returns**:
    -   `str`: The completion response from the API.

### `label(self, payload: dict, api_url: Optional[str] = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct", inputs_column: Optional[str] = "inputs", response_key: Optional[str] = "query", output: Optional[str] = "queries", num_return_sequences: Optional[int] = 3, token_threshold: Optional[int] = 600, validate_payload: bool = False) -> Dataset`

Labels the dataset using the completion client.

-   **Parameters**:
    -   `payload`  (dict): The payload to be sent to the completion API.
    -   `api_url`  (str, optional): The API URL for the completion client (default is "[https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct](https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-70B-Instruct)").
    -   `inputs_column`  (str, optional): The name of the column containing the input text (default is "inputs").
    -   `response_key`  (str, optional): The key to extract the response from the completion client (default is "query").
    -   `output`  (str, optional): The name of the column to store the output (default is "queries").
    -   `num_return_sequences`  (int, optional): The number of response sequences to generate for each input (default is 3).
    -   `token_threshold`  (int, optional): The token threshold for the completion response (default is 600).
    -   `validate_payload`  (bool, optional): Whether to validate the payload before sending (default is False).
-   **Returns**:
    -   `Dataset`: The labeled dataset.

### `select(self, payload: dict, api_url: Optional[str] = "https://api-inference.huggingface.co/models/microsoft/Phi-3-medium-4k-instruct", inputs_column: Optional[str] = "inputs", response_key: Optional[str] = "query", output: Optional[str] = "query", validate_payload: bool = False) -> None`

Selects outputs from the labeled dataset.

-   **Parameters**:
    -   `payload`  (dict): The payload to be sent to the completion API.
    -   `api_url`  (str, optional): The API URL for the completion client (default is "[https://api-inference.huggingface.co/models/microsoft/Phi-3-medium-4k-instruct](https://api-inference.huggingface.co/models/microsoft/Phi-3-medium-4k-instruct)").
    -   `inputs_column`  (str, optional): The name of the column containing the input text (default is "inputs").
    -   `response_key`  (str, optional): The key to extract the response from the completion client (default is "query").
    -   `output`  (str, optional): The name of the column to store the output (default is "query").
    -   `validate_payload`  (bool, optional): Whether to validate the payload before sending (default is False).
-   **Returns**:
    -   `None`

### `to_parquet(self, filepath: str) -> None`

Saves the labeled dataset to a Parquet file.

-   **Parameters**:
    -   `filepath`  (str): The file path to save the Parquet file.
-   **Returns**:
    -   `None`

## Citing this project
If you use this code in your research, please use the following BibTeX entry.

```BibTeX
@misc{louisbrulenaudet2024,
	author = {Louis Brulé Naudet},
	title = {GSPL: Gen-Selective Pseudo Labeler},
	howpublished = {\url{https://github.com/louisbrulenaudet/gspl}},
	year = {2024}
}
```
## Feedback
If you have any feedback, please reach out at [louisbrulenaudet@icloud.com](mailto:louisbrulenaudet@icloud.com).
