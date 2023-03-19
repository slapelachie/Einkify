"""
error.py
author: slapelachie <slapelachie@gmail.com>
"""


class VerifyFileError(Exception):
    """
    Raised when a file fails a verification check.

    Attributes:
        message (str): The error message associated with the exception.
    """

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return f"{self.message}"
