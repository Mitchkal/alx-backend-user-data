#!/usr/bin/env python3
"""
authentication module
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """
    takes in password string and returns it salted and hashed bytes
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


class Auth:
    """
    Auth class to interact with authentication database
    """

    def __init__(self):
        """
        initialization
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        registers a user with a hashed password
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            pass

        hashed_pass = _hash_password(password)
        hashed_password = hashed_pass.decode('utf-8')

        user = self._db.add_user(email=email,
                                 hashed_password=hashed_password)
        return user
