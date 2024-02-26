#!/usr/bin/env python3
"""API Routes for Authentication Service"""
from auth import Auth
from flask import (
                    Flask,
                    jsonify,
                    make_response,
                    request,
                    abort
                  )


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'], strict_slashes=False)
def hello():
    """
    The `hello` function returns a response with a JSON message
    "Bienvenue" and a status code of 200.
    """
    return make_response(jsonify({'message': 'Bienvenue'}), 200)


@app.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    '''
    creating user using Auth module
    '''
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    try:
        AUTH.register_user(email, password)
    except ValueError:
        return make_response(jsonify(
            {"message": "email already registered"}), 400)
    return make_response(jsonify(
        {"email": F"{email}", "message": "user created"}), 200)


@app.route('/sessions',  methods=['POST'], strict_slashes=False)
def login_sessions():
    """
    `login_sessions` function handles user login authentication
    and creates a session cookie upon successful login.
    """
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if not AUTH.valid_login(email, password):
        abort(401)
    resp = make_response(jsonify({"email": F"{email}",
                                  "message": "logged in"}), 200)
    resp.set_cookie('session_id', AUTH.create_session(email))
    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
