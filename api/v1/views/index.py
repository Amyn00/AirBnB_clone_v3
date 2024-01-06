#!/usr/bin/python3
"""Index file to connect to API."""
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
app = Flask(__name__)
app.url_map.strict_slashes = False

@app_views.route('/status')
def status():
    """Return the status of the API."""
    return jsonify({"status": "OK"})
