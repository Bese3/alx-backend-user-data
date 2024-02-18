#!/usr/bin/env python3
"""
Module for handling Personal Data
"""
from typing import List
import re
import logging


def filter_datum(fields: List[str],
                 redaction: str, message: str,
                 separator: str) -> str:
    """
    The function `filter_datum` redacts specified fields
    in a message using a given redaction string and separator.
    """
    my_str = message
    for i in fields:
        pattern = re.search(i + f'[^{separator}]*', message)
        repl = i + '=' + redaction
        my_str = re.sub(pattern.group(0), repl, my_str)
    # my_str = re.sub(';', separator, my_str)
    return my_str


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]) -> None:
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        The `format` function in the given Python code snippet
        redacts sensitive information from a log record before
        formatting it.
        """
        log = super(RedactingFormatter, self).format(record=record)
        return filter_datum(self.fields, self.REDACTION, log, self.SEPARATOR)
