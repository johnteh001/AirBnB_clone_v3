#!/usr/bin/python3
"""app module"""
import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS
from models import storage
from api.v1.views import app_views


app = Flask(__name__)
cors = CORS(app, resources="/*", origins="0.0.0.0")
app.register_blueprint(app_views)


@app.errorhandler(404)
def page_not_found(error):
    """Returns formate response of 404 error"""
    return jsonify({"error": "Not found"}), 404


@app.teardown_appcontext
def close_session(exception):
    """Closes current session"""
    storage.close()


if __name__ == '__main__':
    host = os.getenv('HBNB_API_HOST')
    port = os.getenv('HBNB_API_PORT')
    if host is None:
        host = '0.0.0.0'
    if port is None:
        port = '5000'
    app.run(host, port, threaded=True)
