#!/usr/bin/env python3
'''
view for session authentication
'''
from flask import request, jsonify, make_response
from api.v1.views import app_views
from os import getenv
from models.user import User


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
