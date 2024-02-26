#!/usr/bin/env python3
""" Authentication Module """

import bcrypt
from db import DB
from user import User
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> str:
    """ Returns a salted hash of the input password """
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed


def _generate_uuid() -> str:
    """
    returns a randomly generated UUID.
    """
    return str(uuid4())


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
            hashed_password = _hash_password(password)
            user = self._db.add_user(email, hashed_password)

            return user

        else:
            raise ValueError(f'User {email} already exists')

    def valid_login(self, email: str, password: str) -> bool:
        """
        The function `valid_login` checks if the provided email and
        password match a user's credentials in the database.
        """
        user = None
        try:
            user = self._db.find_user_by(**{'email': email})
        except (InvalidRequestError, NoResultFound):
            return False
        if bcrypt.checkpw(password.encode(), user.hashed_password):
            return True
        return False

    def create_session(self, email: str) -> str:
        """
        `create_session` takes an email, finds the user in the database,
        updates the user's session ID in the database.
        """
        try:
            user = self._db.find_user_by(email=email)
        except (InvalidRequestError, NoResultFound):
            return
        session_id = _generate_uuid()
        self._db.update_user(user.id, **{'session_id': session_id})
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        The function `get_user_from_session_id` retrieves a user from
        the database based on a given session ID.
        """
        try:
            user = self._db.find_user_by(**{'session_id': session_id})
        except (InvalidRequestError, NoResultFound):
            return
        return user

    def destroy_session(self, user_id: int) -> None:
        """Updates the corresponding user's session ID to None"""
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            return None

        self._db.update_user(user.id, session_id=None)

        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        generates a reset password token for a user with a given email
        address and updates the user's information in the database.
        """
        try:
            user = self._db.find_user_by(**{'email': email})
        except (InvalidRequestError, NoResultFound):
            raise ValueError
        res_tk = _generate_uuid()
        self._db.update_user(user.id, **{'reset_token': res_tk})
        return res_tk
