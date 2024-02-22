#!/usr/bin/env python3
'''
session expiration authentication module
'''
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    '''
    session expiration authentication class
    '''
    def __init__(self):
        self.session_duration = 0
        if getenv('SESSION_DURATION') and \
                isinstance(int(getenv('SESSION_DURATION')), int):
            self.session_duration = int(getenv('SESSION_DURATION'))

    def create_session(self, user_id: str = None) -> str:
        """
        The `create_session` function creates a session for a user and
        stores the user ID and creation timestamp in a dictionary.
        """
        s_id = super().create_session(user_id)
        if s_id is None:
            return
        my_dict = {'user_id': user_id, 'created_at': datetime.now()}
        SessionExpAuth.user_id_by_session_id[s_id] = my_dict
        return s_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        This function retrieves the user ID associated with a given session ID,
        taking into account session expiration and creation time.
        """
        if session_id is None:
            return
        if session_id not in SessionExpAuth.user_id_by_session_id.keys():
            return
        my_dict = SessionExpAuth.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return my_dict['user_id']
        if 'created_at' not in my_dict.keys():
            return
        duration = timedelta(seconds=self.session_duration)
        if my_dict['created_at'] + duration < datetime.now():
            return
        return my_dict['user_id']
