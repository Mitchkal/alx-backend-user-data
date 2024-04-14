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


def is_valid(hashed_password: bytes, password: str) -> bool:
    """
    validates tha passord matches hash
    """
    pass_encoded = password.encode()
    if bcrypt.checkpw(pass_encoded, hashed_password):
        return True
    return False
