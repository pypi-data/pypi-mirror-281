# -*- coding: utf-8 -*-
# Copyright (c) Louis Brulé Naudet. All Rights Reserved.
# This software may be used and distributed according to the terms of License Agreement.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
import logging
import time

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

# Set up logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def retry(
    show_error: bool = True
) -> Callable:
    """
    Decorator that retries a function if an exception occurs.

    This decorator catches any exceptions raised by the decorated function
    and retries the function with the same arguments. If the function succeeds,
    it returns the result. If an exception occurs again, it will log the error
    message and retry the function indefinitely.

    Parameters
    ----------
    show_error : bool, optional
        Whether to log the error when an exception occurs (default is True).

    Returns
    -------
    wrapper : callable
        The decorated function.

    Examples
    --------
    >>> @retry(show_error=True)
    ... def divide(a, b):
    ...     return a / b
    ...
    >>> print(divide(10, 2))
    5.0
    >>> print(divide(10, 0))
    ERROR:root:Error occurred: division by zero
    INFO:root:Retrying function with the same parameters...
    ERROR:root:Error occurred: division by zero
    INFO:root:Retrying function with the same parameters...
    ERROR:root:Error occurred: division by zero
    INFO:root:Retrying function with the same parameters...
    (indefinitely retries until stopped)

    Notes
    -----
    This decorator will retry the function indefinitely until it succeeds.
    If you want to limit the number of retries or add additional logic,
    you can modify the decorator accordingly.

    The decorator uses the `functools.wraps` function to preserve the
    metadata of the decorated function (e.g., name, docstring, etc.).
    """
    def decorator_retry(
        func,
    ) -> Callable:
        @functools.wraps(func)
        def wrapper(
            *args,
            **kwargs
        ) -> Callable:
            try:
                return func(
                    *args,
                    **kwargs
                )

            except Exception as e:
                if show_error:
                    logging.error(f"Error occurred: {e}")
                    logging.info("Retrying function with the same parameters...")

                return wrapper(
                    *args,
                    **kwargs
                )
        return wrapper
    return decorator_retry


def rate_limit(
    rpm: Optional[int]=30
) -> Callable:
    """
    Decorator to enforce a rate limit on function calls.

    This decorator ensures that a function is not called more than a specified
    number of times per minute (RPM). It achieves this by calculating the minimum
    interval between calls and adding a delay if the function is called too quickly.

    Parameters
    ----------
    rpm : int
        The maximum number of allowed function calls per minute.

    Returns
    -------
    function
        A decorator that limits the rate of function calls to the specified RPM.

    Examples
    --------
    >>> @rate_limit(30)
    ... def my_function():
    ...     print("Function called")
    ...
    >>> my_function()  # Function calls will be limited to 30 per minute
    """
    min_interval: float = 60.0 / rpm

    def decorator(
        func: Callable
    ) -> Callable:
        """
        Inner decorator function that wraps the target function to enforce rate limiting.

        Parameters
        ----------
        func : function
            The function to be wrapped by the rate limiting decorator.

        Returns
        -------
        function
            The wrapped function with rate limiting applied.
        """
        last_exec_time: int = 0

        @functools.wraps(func)
        def wrapper(
            *args, 
            **kwargs
        ) -> Any:
            """
            Wrapper function to enforce the rate limit.

            Parameters
            ----------
            *args : tuple
                Positional arguments to pass to the wrapped function.

            **kwargs : dict
                Keyword arguments to pass to the wrapped function.

            Returns
            -------
            Any
                The return value of the wrapped function.
            """
            nonlocal last_exec_time

            elapsed_time: float = time.perf_counter() - last_exec_time
            
            if elapsed_time < min_interval:
                time.sleep(min_interval - elapsed_time)
            
            result: Any = func(*args, **kwargs)
            last_exec_time = time.perf_counter()

            return result
        
        return wrapper

    return decorator