#!/usr/bin/env python3
"""
Basic Authentication
"""

from api.v1.auth.auth import Auth
import base64


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
        and returns it decoded
        """
        if authorization_header is None:
            return None
        if type(authorization_header) is not str:
            return None
        if not authorization_header.startswith("Basic "):
            return None
        encoded = authorization_header.split(' ')[1]
        return encoded

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str
                                           ) -> str:
        """
        returns decoded base64 string
        """
        if base64_authorization_header is None:
            return None
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            encoded_bytes = base64_authorization_header.encode('utf-8')
            converted_bytes = base64.b64decode(encoded_bytes)
            decoded = converted_bytes.decode('utf-8')

        except BaseException as e:
            return None

        return decoded
