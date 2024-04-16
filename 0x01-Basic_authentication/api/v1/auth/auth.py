#!/usr/bin/env python3
"""
Class to manage authentication
"""
from flask import request
from typing import List, TypeVar


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
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        if not path.endswith('/'):
            path += '/'

        for excluded_path in excluded_paths:
            if not excluded_path.endswith('/'):
                excluded_path += '/'

            if path == excluded_path:
                return False

        return True

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
