#!/usr/bin/env python3
'''
Session Authentication module
'''
from api.v1.auth.auth import Auth
from uuid import uuid4


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
