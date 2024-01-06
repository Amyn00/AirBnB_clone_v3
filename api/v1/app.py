#!/usr/bin/python3
"""Connect to API"""
import os
from models import storage
from api.v1.views import app_views
from flask import Flask, Blueprint


app = Flask(__name__)
app.register_blueprint(app_views, url_prefix='/api/v1')


@app.teardown_appcontext
def teardown_appcontext(exception):
    """Closes the storage."""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """Handler for 404 errors, returns a JSON-formatted response."""
    return make_response(jsonify({"error": "Not found"}), 404)


if __name__ == "__main__":
    host = os.getenv('HBNB_API_HOST', '0.0.0.0')
    port = int(os.getenv('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
