#!/usr/bin/env python3
'''
Session Authentication module
'''
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    '''
    Session Authentication class
    '''
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        The function `create_session` generates a session ID and
        associates it with a user ID in a dictionary.
        """
        if user_id is None:
            return
        if not isinstance(user_id, str):
            return
        session_id = str(uuid4())
        SessionAuth.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        This function retrieves the user ID associated with
        a given session ID.
        """
        if session_id is None:
            return
        if not isinstance(str(session_id), str):
            return
        return SessionAuth.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None):
        """
        This Python function retrieves the current user based on
        the session ID provided in the request.
        """
        session_id = self.session_cookie(request)
        if session_id is None:
            return
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return
        user = User.get(user_id)
        return user
