# -*- coding: utf-8 -*-
# Copyright (c) Louis Brulé Naudet. All Rights Reserved.
# This software may be used and distributed according to the terms of License Agreement.
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import time
from threading import Lock


class Logger:
    """
    A class to redirect stdout to a log file while also writing to the terminal.

    Attributes
    ----------
    terminal_stdout : file object
        The original standard output (terminal).

    log : file object
        The log file where the output is written.

    lock : Lock
        A lock to ensure thread-safe operations.

    Methods
    -------
    write(message)
        Writes the message to both the terminal and the log file.

    flush()
        Flushes the output streams.

    close()
        Closes the log file.

    isatty()
        Checks if the terminal is a TTY device.
    """
    def __init__(self, filename:str, terminal_stdout):
        """
        Initializes Logger with a file to log the output.

        Parameters
        ----------
        filename : str
            The name of the file to write the log.
        terminal_stdout : file object
            The standard output stream to use (typically sys.stdout).
        """
        self.terminal_stdout = terminal_stdout
        self.log = open(filename, "w")
        self.lock = Lock()

    def write(self, message:str):
        """
        Writes a message to the terminal and the log file.

        Parameters
        ----------
        message : str
            The message to write.
        """
        with self.lock:
            self.terminal_stdout.write(message)
            self.log.write(message)

    def flush(self):
        """
        Flushes the output streams to ensure all data is written.
        """
        with self.lock:
            self.terminal_stdout.flush()
            self.log.flush()

    def close(self):
        """
        Closes the log file.
        """
        with self.lock:
            self.log.close()

    def isatty(self):
        """
        Checks if the terminal is a TTY device.
        """
        return self.terminal_stdout.isatty()


class StdErrLogger(Logger):
    """
    A class to redirect stderr to a log file while also writing to the terminal.

    Inherits from Logger.
    
    Methods
    -------
    write(message)
        Writes the message to both the terminal and the log file.

    flush()
        Flushes the output streams.

    isatty()
        Checks if the terminal is a TTY device.
    """
    def __init__(self, filename:str, terminal_stderr):
        """
        Initializes StdErrLogger with a file to log the output.

        Parameters
        ----------
        filename : str
            The name of the file to write the log.
        terminal_stderr : file object
            The standard error stream to use (typically sys.stderr).
        """
        super().__init__(filename, terminal_stderr)
        self.terminal_stderr = terminal_stderr

    def write(self, message:str):
        """
        Writes a message to the terminal and the log file.

        Parameters
        ----------
        message : str
            The message to write.
        """
        with self.lock:
            self.terminal_stderr.write(message)
            self.log.write(message)

    def flush(self):
        """
        Flushes the output streams to ensure all data is written.
        """
        with self.lock:
            self.terminal_stderr.flush()
            self.log.flush()

    def isatty(self):
        """
        Checks if the terminal is a TTY device.
        """
        return self.terminal_stderr.isatty()
