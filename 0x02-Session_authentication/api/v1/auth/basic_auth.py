#!/usr/bin/env python3
""" Module of Basic Authentication
"""
from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


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
        return decoded.decode()

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

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """
        This function takes user email and password as input, searches
        for a user with the provided email, and returns the user object
        if the password is valid.
        """
        if user_email is None or not isinstance(user_email, str):
            return
        if user_pwd is None or not isinstance(user_pwd, str):
            return

        found_users = None
        try:
            found_users = User.search({'email': user_email})
        except Exception:
            pass

        if found_users is None:
            return

        for f in found_users:
            if f.is_valid_password(user_pwd):
                return f
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        The function `current_user` extracts user credentials from an
        authorization header and returns the corresponding user object.
        """
        auth_header = self.authorization_header(request)
        if auth_header is None:
            return

        extract = self.extract_base64_authorization_header(auth_header)
        if extract is None:
            return

        decode = self.decode_base64_authorization_header(extract)
        if decode is None:
            return

        user_email, user_pwd = self.extract_user_credentials(decode)
        if user_email is None or user_pwd is None:
            return

        obj = self.user_object_from_credentials(user_email, user_pwd)
        return obj
