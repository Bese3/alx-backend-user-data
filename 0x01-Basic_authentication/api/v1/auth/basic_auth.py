#!/usr/bin/env python3
""" Module of Basic Authentication
"""
from api.v1.auth.auth import Auth
import base64


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

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        The function decodes a base64-encoded authorization header and
        returns the decoded string in UTF-8 format.
        """
        if base64_authorization_header is None:
            return
        if not isinstance(base64_authorization_header, str):
            return
        decoded = ""
        try:
            decoded = base64.b64decode(base64_authorization_header)
        except Exception:
            return
        return decoded.decode('utf-8')

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        The function `extract_user_credentials` takes a decoded base64
        authorization header and returns the username and password
        separated by a colon.
        """
        if decoded_base64_authorization_header is None:
            return None, None
        if not isinstance(decoded_base64_authorization_header, str):
            return None, None
        if ':' not in decoded_base64_authorization_header:
            return None, None
        separated = decoded_base64_authorization_header.split(":", 1)

        return separated[0], separated[1]
