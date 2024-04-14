#!/usr/bin/env python3
"""
Password encryption
"""
import bcrypt
import base64


def hash_password(password: str) -> bytes:
    """
    returns a salted, hashed password
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed
