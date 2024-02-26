#!/usr/bin/env python3
"""API Routes for Authentication Service"""
# from auth import Auth
from flask import Flask, jsonify, make_response


app = Flask(__name__)


@app.route('/', methods=['GET'], strict_slashes=False)
def hello():
    """
    The `hello` function returns a response with a JSON message
    "Bienvenue" and a status code of 200.
    """
    return make_response(jsonify({'message': 'Bienvenue'}), 200)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
