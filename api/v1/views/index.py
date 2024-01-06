#!/usr/bin/python3
"""Index file to connect to API."""
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify
app = Flask(__name__)
app.url_map.strict_slashes = False


@app_views.route('/stats')
def get_stats():
    """Retrive the number of each object by type."""
    stats = {
        'amenities': storage.count('Amenity'),
        'cities': storage.count('City'),
        'places': storage.count('Place'),
        'reviews': storage.count('Review'),
        'states': storage.count('State'),
        'users': storage.count('User')
    }
    return jsonify(stats)


@app_views.route('/status')
def status():
    """Return the status of the API."""
    return jsonify({"status": "OK"})
