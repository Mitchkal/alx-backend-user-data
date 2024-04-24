#!/usr/bin/env python3
"""
Basic flask implementation
"""

from flask import Flask, jsonify, abort


app = Flask(__name__)


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    """
    index module
    """
    return jsonify({"message": "BienVenue"})


if __name__ == "__main__":
    """
    the main function
    """
    app.run(host="0.0.0.0", port="5000")
