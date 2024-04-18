#!/usr/bin/env python3
"""
Basic Authentication
"""

from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """
    inherits from class Auth
    """

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

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str
                                 ) -> str:
        """
        extracts the user emails and passwords from base64encoded value
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        credentials = decoded_base64_authorization_header.split(':', 1)
        return credentials[0], credentials[1]

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        returns user instance based on email and password
        """
        if user_email is None or not isinstance(user_email, str):
            return None
        if user_pwd is None or not isinstance(user_pwd, str):
            return None
        try:
            exist_user = User.search({'email': user_email})

        except Exception as e:
            return None

        for user in exist_user:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        retrieves user instance for request with basic authentication
        """
        encoded = self.authorization_header(request)

        encoded_user = self.extract_base64_authorization_header(encoded)

        if not encoded_user:
            return None
        decoded_user = self.decode_base64_authorization_header(encoded_user)

        if not decoded_user:
            return None
        email, pwd = self.extract_user_credentials(decoded_user)

        if not email or not pwd:
            return None
        user = self.user_object_from_credentials(email, pwd)
        return user
