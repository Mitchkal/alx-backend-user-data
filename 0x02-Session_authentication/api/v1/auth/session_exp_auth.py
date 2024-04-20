#!/usr/bin/env python3
"""
Module for session expiration
"""
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    Session expiration class
    """
    def __init__(self):
        """
        initialization
        """
        super().__init__()
        self.session_duration = int(getenv("SESSION_DURATION", "0"))

    def create_session(self, user_id=None):
        """
        Creates a session Id
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        user_id_by_session_id = self.user_id_by_session_id

        user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        retrieves user id from session dictionary
        """
        if session_id is None:
            return None

        user_id_by_session_id = self.user_id_by_session_id
        session_data = user_id_by_session_id.get(session_id)

        if session_data is None:
            return None

        session_dict = session_data
        user_id = session_dict.get("user_id")

        if self.session_duration <= 0:
            return user_id

        if "created_at" not in session_dict.keys():
            return None

        created_at = session_dict.get("created_at")
        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if expiration_time < datetime.now():
            return None

        return user_id
