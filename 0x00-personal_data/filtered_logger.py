#!/usr/bin/env python3
"""
Log filtering with regex
"""
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    filters log message to redact info
    """
    pattern = '|'.join(f"{field}=[^{separator}]*" for field in fields)
    return re.sub(pattern,
                  lambda match: match.group().split('=')[0] + f'={redaction}',
                  message)
