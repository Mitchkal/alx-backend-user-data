#!/usr/bin/env python3
"""
Basic flask implementation
"""

from flask import Flask, jsonify, request, make_response, abort
from auth import Auth


Auth = Auth()
app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    index module
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    """
    endpoint o register user
    """

    email = request.form.get("email", type=str)
    password = request.form.get("password", type=str)

    try:
        Auth.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})

    except ValueError as err:
        return jsonify({"message": "email already registered"}), 400


@app.route('/sessions', methods=["POST"], strict_slashes=False)
def login() -> str:
    """
    endpoint for the login session
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if email is None or password is None:
        abort(400)

    if Auth.valid_login(email, password):
        session_id = Auth.create_session(email)
        res = jsonify({"email": email, "message": "logged in"})

        res.set_cookie("session_id", session_id)
        return res
    abort(401)


if __name__ == "__main__":
    """
    the main function
    """
    app.run(host="0.0.0.0", port="5000")
