#!/usr/bin/env python3
""" Module of Authentication
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Authorization class starts here
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        checks if url needs authenthication
        """
        return False

    def authorization_header(self, request=None) -> str:
        """
        sets authorization header
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        checks current user
        """
        return None
