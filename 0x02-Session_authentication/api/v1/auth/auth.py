#!/usr/bin/env python3
""" Module of Authentication
"""
from flask import request
from typing import List, TypeVar
from os import getenv


class Auth:
    """
    Authorization class starts here
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        checks if url needs authenthication
        """
        if path is None or excluded_paths is None or excluded_paths == []:
            return True
        if path[-1] != '/':
            path += '/'
        if path == '/api/v1/status/' and path in excluded_paths:
            return False
        if path not in excluded_paths:
            return True
        if path in excluded_paths:
            return False
        return False

    def authorization_header(self, request=None) -> str:
        """
        sets authorization header
        """
        if request is None:
            return None
        if request.headers.get('Authorization', None):
            return request.headers['Authorization']
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        checks current user
        """
        return None

    def session_cookie(self, request=None):
        """
        The function `session_cookie` retrieves a session cookie
        from a request object using the session name obtained from
        the environment variables.
        """
        if request is None:
            return
        my_session = getenv('SESSION_NAME')
        return request.cookies.get(my_session)
