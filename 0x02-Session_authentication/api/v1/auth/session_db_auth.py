#!/usr/bin/env python3
'''
session authentication using database
'''
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import timedelta, datetime


class SessionDBAuth(SessionExpAuth):
    '''
    DB session authentication class
    '''

    def create_session(self, user_id: str = None) -> str:
        """
        The function `create_session` creates a new user
        session and saves it.
        """
        if user_id is None:
            return
        s_id = super().create_session(user_id)
        user_session = UserSession(user_id=user_id, session_id=s_id)
        user_session.save()
        return s_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        This function is intended to retrieve the user ID associated with a
        given session ID, considering session duration and timestamp.
        """
        if session_id is None:
            return
        UserSession.load_from_file()
        user = UserSession.search({'session_id': session_id})
        if user is None:
            return
        t1 = user[0].created_at
        t2 = timedelta(seconds=self.session_duration)
        # print(f"t1 = {t1}, t1 + t2 = {t1 + t2}")
        # print((t1 + t2) < datetime.now())
        if (t1 + t2) < datetime.now():
            return
        return user[0].user_id

    def destroy_session(self, request=None):
        """
        The function `destroy_session` is designed to remove a user
        session based on the session ID provided in the request.
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        u_id = self.user_id_for_session_id(session_id)
        if u_id is None:
            return False
        user = UserSession.search({'session_id': session_id})
        try:
            user[0].remove()
            UserSession.save_to_file()
        except Exception:
            return False
        return True
