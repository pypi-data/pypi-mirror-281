# -*- coding: utf-8 -*-
# Copyright (c) Louis Brulé Naudet. All Rights Reserved.
# This software may be used and distributed according to the terms of License Agreement.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from typing import (
    IO,
    TYPE_CHECKING,
    Any,
    Dict,
    List,
    Iterator,
    Type,
    Tuple,
    Union,
    Mapping,
    TypeVar,
    Callable,
    Optional,
    Sequence,
)

from nltk.tokenize import sent_tokenize


class TextSplitter:
    def __init__(
        self, 
        text: str
    ):
        """
        A class to split text recursively into chunks of specified size using NLTK.

        Attributes
        ----------
        text : str
            The input text to be split into chunks.

        Methods
        -------
        split_text(chunk_size: int, language: str = "french") -> list:
            Splits the input text into chunks of a specified size using NLTK.
        """
        self.text:str = text


    def split_text(
        self, 
        max_chunk_size: Optional[int] = 2500, 
        min_chunk_size: Optional[int] = 800, 
        language: str = "french"
    ) -> list:
        """
        Splits the input text into chunks of a specified size using NLTK.

        Parameters
        ----------
        max_chunk_size : int, optional
            The maximum size limit for each chunk. Default is 2500.

        min_chunk_size : int, optional
            The minimum size limit for each chunk. Default is 800.

        language : str, optional
            The language used for sentence tokenization. Default is "french".

        Returns
        -------
        split_text : list
            A list of text chunks with approximately specified size.
        """
        if not isinstance(self.text, str):
            raise ValueError("Input text must be a string")

        if not (isinstance(max_chunk_size, int) and isinstance(min_chunk_size, int)):
            raise ValueError("Chunk size should be integers")

        if max_chunk_size <= 0 or min_chunk_size <= 0:
            raise ValueError("Chunk sizes should be positive integers")

        # Tokenize sentences using NLTK for the specified language
        sentences: list = sent_tokenize(
            self.text, 
            language=language
        )

        chunks: list = []
        current_chunk: str = ""

        for sentence in sentences:
            if len(current_chunk) + len(sentence) <= max_chunk_size:
                current_chunk += sentence
                
            else:
                if len(current_chunk) >= min_chunk_size:
                    chunks.append(current_chunk)
                    current_chunk:str = sentence
                else:
                    remaining_space:int = min_chunk_size - len(current_chunk)
                    current_chunk += sentence[:remaining_space]
                    chunks.append(current_chunk)
                    current_chunk:str = sentence[remaining_space:]

        if current_chunk:
            chunks.append(current_chunk)

        # Remove empty strings from the list
        split_text:list = list(filter(None, chunks))

        return split_text