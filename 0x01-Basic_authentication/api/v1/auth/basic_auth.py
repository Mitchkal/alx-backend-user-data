#!/usr/bin/env python3
"""
Basic Authentication
"""

from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    inherits from class Auth
    """
    def __init__(self):
        """
        initialization
        """
        super().__init__()
        pass

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        extracts the base64 part of Authorization header
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        encoded = authorization_header.split(' ')[1]
        return encoded
