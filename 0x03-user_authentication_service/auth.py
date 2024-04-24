#!/usr/bin/env python3
"""
authentication module
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """
    takes in password string and returns it salted and hashed bytes
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed
