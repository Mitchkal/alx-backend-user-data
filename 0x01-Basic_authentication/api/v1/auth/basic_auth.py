#!/ust/bin/env python3
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
