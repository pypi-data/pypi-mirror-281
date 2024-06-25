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

from tqdm import tqdm
import tiktoken

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


class Token():
    def __init__(
        self, 
        text: str, 
        model: Optional[str] = "cl100k_base", 
        cost: Optional[float] = 0.0015, 
        dimension: Optional[int] = 1000
    ):
        """
        Token class for estimating token-based costs and counting tokens in text data.
        
        This class is designed to estimate the cost of processing tokens in text data
        and count the number of tokens in the provided data.

        Parameters
        ----------
        text : str
            The text content to process.
          
        model : str
            The token encoding used for analysis (set to "cl100k_base" by default).

        cost : float
            The cost per specific number of tokens (default value is 0.0015).

        dimension : int
            The dimension of the token space (default value is 1000).
        """
        self.text: str = text
        self.model: str = model
        self.cost: float = cost
        self.dimension:int = dimension


    def cost_estimation(
        text: Union[str, List[str]], 
        model: Optional[str] = "cl100k_base", 
        cost: Optional[float] = 0.0015, 
        dimension: Optional[int] = 1000
    ) -> float:
        """
        Estimate the total cost of processing tokens.

        This method estimates the total cost based on the cost per token and
        the dimension of the token space.

        Parameters
        ----------
        text : Union[str, List[str]]
            The text content or list of text contents to process.
          
        model : str
            The token encoding used for analysis (set to "cl100k_base" by default).

        cost : float
            The cost per specific number of tokens (default value is 0.0015).

        dimension : int
            The dimension of the token space (default value is 1000).

        Returns
        -------
        estimated_cost : float
            The estimated total cost.
        """
        num_tokens: int = Token.count(
            text, 
            model
        )

        estimated_cost: float = cost * (num_tokens / dimension)

        return estimated_cost


    @staticmethod
    def count(
        text: Union[str, List[str]], 
        model: Optional[str] = "cl100k_base"
    ) -> int:
        """
        Count the number of tokens in the provided text element or list of text elements.

        This method counts the number of tokens in the provided text element(s)
        using the token encoding.

        Parameters
        ----------
        text : Union[str, List[str]]
            The text content or list of text contents to process.

        model : str
            The token encoding used for analysis (set to "cl100k_base" by default).

        Returns
        -------
        num_tokens : int
            The number of tokens in the text element(s).
        """
        if isinstance(text, str):
            text = [text]  # Convert single string to list for uniform processing
        
        encoding: Any = tiktoken.get_encoding(model)
        
        num_tokens: int = sum(
            len(encoding.encode(t)) for t in text
        )

        return num_tokens