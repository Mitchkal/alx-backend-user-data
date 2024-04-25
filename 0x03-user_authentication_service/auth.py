#!/usr/bin/env python3
"""
authentication module
"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """
    takes in password string and returns it salted and hashed bytes
    """
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed


def _generate_uuid() -> str:
    """
    generates a new uuid in string format
    """
    return str(uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """
        locates user by email and if found,
        checks password
        """
        if email is None or password is None:
            return False
        try:
            user = self._db.find_user_by(email=email)

        except NoResultFound:
            return False

        hashed_password = user.hashed_password.encode('utf-8')

        encoded_pass = password.encode('utf-8')

        if bcrypt.checkpw(encoded_pass, hashed_password):
            return True

        return False

    def create_session(self, email: str) -> str:
        """
        finds user corresponding to email,
        generates new uuid,
        and stores it as user's session id
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception as e:
            pass

    def get_user_from_session_id(self, session_id: str):
        """
        retrieves a user based by their session id or none
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user

        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        destroys a user session  identified by the user id
        """
        if user_id is not None:
            self._db.update_user(user_id, "session_id"=None)

        return None
