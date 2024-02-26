#!/usr/bin/env python3
""" Authentication Module """

import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> str:
    """ Returns a salted hash of the input password """
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        The function `register_user` checks if a user with the given email
        already exists, hashes the password if necessary, and adds a
        new user to the database.
        """
        user = None
        try:
            user = self._db.find_user_by(**{'email': email})
        except (InvalidRequestError, NoResultFound):
            pass
        if user is not None:
            raise ValueError(F'user {user.email} already exists')
        if not isinstance(password, bytes):
            password = _hash_password(password)
        self._db.add_user(email, password)
        return user
