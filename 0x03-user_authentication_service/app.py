#!/usr/bin/env python3
"""
Basic flask implementation
"""

from flask import Flask, jsonify, request, make_response, abort, redirect
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
    email = request.form.get("email", '')
    password = request.form.get("password", '')

    if email == '' or password == '':
        abort(400)

    if Auth.valid_login(email, password):
        session_id = Auth.create_session(email)
        res = jsonify({"email": email, "message": "logged in"})

        res.set_cookie("session_id", session_id)
        return res
    abort(401)


@app.route('/sessions', methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    """
    responds to the sessions route by destroying session id
    and redirecting user to the GET /
    """
    session_id = request.cookies.get("session_id", None)

    if session_id is None:
        abort(403)

    user = Auth.get_user_from_session_id(session_id)

    if user is None:
        abort(403)

    Auth.destroy_session(user.id)

    response = redirect('/')
    response.delete_cookie("session_id")
    return response


@app.route('/profile', methods=['GET'], strict_slashes=False)
def profile() -> str:
    """
    endpoint for the user profile
    """
    session_id = request.cookies.get('session_id', None)

    if session_id is not None:
        user = Auth.get_user_from_session_id(session_id)

        if user is not None:
            return jsonify({"email": user.email}), 200

    abort(403)


@app.route('/reset_password', methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """
    endpoint to reset password
    """
    email = request.form.get("email")
    if email is None:
        abort(403)

    try:
        reset_token = Auth.get_reset_password_token(email)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "reset_token": reset_token}), 200


if __name__ == "__main__":
    """
    the main function
    """
    app.run(host="0.0.0.0", port="5000")
