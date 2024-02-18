#!/usr/bin/env python3
"""
Module for handling Personal Data
"""
from typing import List
import re


def filter_datum(fields: List[str],
                 redaction: str, message: str,
                 separator: str) -> str:
    """
    The function `filter_datum` redacts specified fields
    in a message using a given redaction string and separator.
    """
    my_str = message
    for i in fields:
        pattern = re.search(i + '[^;]*', message)
        repl = i + '=' + redaction
        my_str = re.sub(pattern.group(0), repl, my_str)
    my_str = re.sub(';', separator, my_str)
    return my_str
