#!/usr/bin/env python3
"""API Routes for Authentication Service"""
from auth import Auth
from flask import (
                    Flask,
                    jsonify,
                    make_response,
                    request,
                    abort,
                    redirect
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


@app.route('/sessions', methods=['DELETE'], strict_slashes=False)
def logout_sessions():
    """
    `logout_sessions` logs out a user by destroying their session and
    redirecting them to the homepage.
    """
    s_id = request.cookies.get('session_id', None)
    if s_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(s_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect('/')


@app.route('/profile', methods=['GET'], strict_slashes=False)
def get_profile():
    """
    `get_profile` retrieves the email of a user based on their
    session ID stored in a cookie.
    """
    s_id = request.cookies.get('session_id', None)
    if s_id is None:
        abort(403)
    user = AUTH.get_user_from_session_id(s_id)
    if user is None:
        abort(403)
    return make_response(jsonify({'email': user.email}), 200)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def reset_password_token():
    """
    `reset_password_token()` is returning a JSON response with the
    email and reset token in the format:
    ```json
    {
        "email": "example@example.com",
        "reset_token": "generated_reset_token"
    }
    ```
    The HTTP status code returned is 200 (OK).
    """
    email = request.form.get('email', None)
    if email is None:
        abort(403)
    try:
        rest_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return make_response(jsonify({"email": email,
                                  "reset_token": rest_token}), 200)


@app.route('/reset_password', methods=['PUT'], strict_slashes=False)
def update_password():
    """
    The function `update_password` updates a user's password using a
    reset token and returns a JSON response.
    """
    email = request.form.get('email', None)
    reset_token = request.form.get('reset_token', None)
    password = request.form.get('new_password', None)
    if not email or not reset_token or not password:
        abort(400)
    try:
        AUTH.update_password(reset_token, password)
    except ValueError:
        abort(403)
    return make_response(jsonify({"email": email,
                                  "message": "Password updated"}), 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
