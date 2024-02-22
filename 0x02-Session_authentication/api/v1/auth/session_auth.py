#!/usr/bin/env python3
'''
Session Authentication module
'''
from api.v1.auth.auth import Auth
from flask import request, jsonify, make_response
from os import getenv
from uuid import uuid4
from models.user import User
from api.v1.views import app_views


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


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """
    handles user authentication by checking the provided email and password.
    """
    email = request.form.get('email', None)
    pwd = request.form.get('password', None)
    if email is None:
        return make_response(jsonify({"error": "email missing"}), 400)
    if pwd is None:
        return make_response(jsonify({"error": "password missing"}), 400)
    found_users = None
    try:
        found_users = User.search({'email': email})
    except Exception:
        pass
    if found_users is None or found_users == []:
        return make_response(jsonify({"error":
                                      "no user found for this email"}), 404)
    for user in found_users:
        if user.is_valid_password(pwd):
            from api.v1.app import auth
            s_id = auth.create_session(user.id)
            u = jsonify(user.to_json())
            u.set_cookie(getenv('SESSION_NAME'), s_id)
            return make_response(u, 200)

    return make_response(jsonify({"error": "wrong password"}), 401)
