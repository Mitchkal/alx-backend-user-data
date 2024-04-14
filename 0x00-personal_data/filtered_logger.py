#!/usr/bin/env python3
"""
Log filtering with regex
"""
import os
import re
from typing import List, Tuple
import logging
import mysql.connector


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
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    stream_handler = logging.StreamHandler()
    redacting_formatter = RedactingFormatter(list(PII_FIELDS))
    stream_handler.setFormatter(redacting_formatter)
    logger.addHandler(stream_handler)

    return logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """
    returns connector to mysql database
    """
    mydb = mysql.connector.connection.MySQLConnection(
            user=os.environ.get("PERSONAL_DATA_DB_USERNAME", "root"),
            password=os.environ.get("PERSONAL_DATA_DB_PASSWORD", ""),
            host=os.environ.get("PERSONAL_DATA_DB_HOST", "localhost"),
            database=os.environ.get("PERSONAL_DATA_DB_NAME")
            )
    return mydb


def main():
    """
    obtains database connection and retrieves all rows in user table
    then displays each row under filtered format
    """

    db = get_db()

    cursor = db.cursor()
    cursor.execute("SELECT * FROM users;")
    names = [i[0] for i in cursor.description]

    logger = get_logger()

    for row in cursor:
        row_str = ''.join(f"{f}={str(r)}; " for r, f in zip(row, names))
        logger.info(row_str.strip())

    cursor.close()
    db.close()


if __name__ == '__main__':
    """
    runs the main function
    """
    main()
