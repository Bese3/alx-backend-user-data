#!/usr/bin/env python3
""" Module of Basic Authentication
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Basic Authentication class
    """
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        The function extracts the base64 encoded authorization
        credentials from an authorization header string starting
        with "Basic ".
        """
        if authorization_header is None:
            return
        if not isinstance(authorization_header, str):
            return
        if not authorization_header.startswith("Basic "):
            return
        encoded = authorization_header.split(" ", 1)[1]
        return encoded
