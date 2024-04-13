#!/usr/bin/env python3
"""
Log filtering with regex
"""
import re
from typing import List, Tuple
import logging


PII_FIELDS: Tuple[str, ...] = ('name', 'email', 'phone', 'ssn', 'password')


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    filters log message to redact info
    """
    pattern = '|'.join(f"{field}=[^{separator}]*" for field in fields)
    return re.sub(pattern,
                  lambda match: match.group().split('=')[0] + f'={redaction}',
                  message)


class RedactingFormatter(logging.Formatter):
    """
    Redacting Formatter class
    """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        initialization
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        the formatter
        """
        record.msg = filter_datum(self.fields, self.REDACTION,
                                  record.msg, self.SEPARATOR)
        return super().format(record)


def get_logger() -> logging.Logger:
    """
    returns logging object
    """
    logging = logging.getlogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    redacting_formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(redacting_Formatter)
    logger.addHandler(stream_handler)

    return logger
