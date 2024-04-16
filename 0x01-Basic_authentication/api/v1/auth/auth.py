#!/usr/bin/env python3
"""
Class to manage authentication
"""
from flask import request


class Auth:
    """
    the authentication class
    """

    def __init__(self):
        """
        initialization
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Returns false
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns None
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns None
        """
        return None
