#!/usr/bin/env python3
"""
Module for handling Personal Data
"""
from typing import List, Tuple
import re
import logging
import mysql.connector
from os import getenv

PII_FIELDS: Tuple[str] = ("name", "email", "phone", "ssn", "password")


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

    def __init__(self, fields: List[str]):
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


def get_logger() -> logging.Logger:
    """
    The function `get_logger` returns a logging object
    configured to redact sensitive information before
    outputting to the stream.
    """
    logger = logging.getLogger('user_data')

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(fields=PII_FIELDS))
    logger.setLevel(logging.INFO)

    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.propagate = False

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    This function establishes a connection to a MySQL database using
    environment variables for host, database name, username, and password.
    """
    ms = mysql.connector.connect(
                                 host=getenv('PERSONAL_DATA_DB_HOST'),
                                 database=getenv('PERSONAL_DATA_DB_NAME'),
                                 user=getenv('PERSONAL_DATA_DB_USERNAME'),
                                 password=getenv('PERSONAL_DATA_DB_PASSWORD'),
                                 auth_plugin='mysql_native_password'
                                 )
    return ms


def main():
    '''
    main function starts here
    '''
    db = get_db()
    cursor = db.cursor()
    logger = get_logger()
    cursor.execute('SELECT * FROM users;')
    rows = cursor.fetchall()
    for r in rows:
        msg = F"name={r[0]}; email={r[1]};\
                phone={r[2]}; ssn={r[3]}; password={r[4]};\
                ip={r[5]}; last_login={r[6]}; user_agent={r[6]};"
        logger.info(msg)
    cursor.close()
    db.close()


if __name__ == '__main__':
    main()

