#!/usr/bin/env python3
"""
Basic flask implementation
"""

from flask import Flask, jsonify, request
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


if __name__ == "__main__":
    """
    the main function
    """
    app.run(host="0.0.0.0", port="5000")