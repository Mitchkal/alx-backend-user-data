#!/usr/bin/env python3
"""
view to handle routes for session authentication
"""
from flask import abort, jsonify, request
from os import getenv
from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """
    method for login
    """
    email = request.form.get('email')

    if email is None:
        return jsonify({"error": "email missing"}), 400

    password = request.form.get("password")

    if password is None:
        return jsonify({"error": "password missing"}), 400

    try:
        user_found = User.search({'email': email})
    except Exception as e:
        return jsonify({"error": "no user found for this email"}), 404
    if not user_found:
        return jsonify({"error": "no user found for this email"}), 404

    for user in user_found:
        if not user.is_valid_password(password):
            return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    print(f"user found is {user_found}")
    user = user_found[0]
    session_id = auth.create_session(user.id)

    SESSION_NAME = getenv("SESSION_NAME")

    response = jsonify(user.to_json())
    response.set_cookie(SESSION_NAME, session_id)

    return response
