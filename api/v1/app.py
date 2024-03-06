#!/usr/bin/python3
"""Contains a Flask API.
"""

import os
from api.v1.views import appi
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import storage

revoked_tokens = set()

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.register_blueprint(appi)
CORS(app, resources={'/*': {'origins': os.getenv('ETA_API_HOST', '0.0.0.0')}})

jwt = JWTManager(app)

@app.teardown_appcontext
def teardownflask(e):
    """End event listener.
    """
    storage.close()


@app.errorhandler(404)
def error_404(err):
    """Handles the 404 HTTP error.
    """
    return jsonify(err="Not found"), 404


if __name__ == "__main__":
    app.run(
            host=os.getenv('ETA_API_HOST', '0.0.0.0'),
            port=int(os.getenv('ETA_API_PORT', '5000')),
            threaded=True
            )
