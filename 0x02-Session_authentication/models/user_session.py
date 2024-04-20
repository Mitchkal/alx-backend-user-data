#!/usr/bin/env python3
"""
module for session id storage
"""
from models.base import Base


class UserSession(Base):
    """
    model for user session storage
    """

    def __init__(self, *args: list, **kwargs: dict):
        """
        class initialization
        """
        super().__init__(*args, **kwargs)

        if kwargs.get("user_id") is not None:
            self.user_id = kwargs.get("user_id")

        if kwargs.get("session_id") is not None:
            self.session_id = kwargs.get("session_id")
