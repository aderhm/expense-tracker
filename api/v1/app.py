#!/usr/bin/python3
"""Contains a Flask API.
"""

import os
from api.v1.views import appi
from datetime import timedelta
from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import storage
from models.token_block_list import TokenBlockList

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=365)
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


@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_data):
    return jsonify({
        "error": "token_expired",
        "message": "Token has expired"
        }), 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        "error": "invalid_token",
        "message": "Signature verification failed"
        }), 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "error": "authorization_required",
        "message": "Token is missing"
        }), 401


@jwt.token_in_blocklist_loader
def token_in_blocklist_callback(jwt_header, jwt_data):
    jti = jwt_data['jti']
    token = storage.get_token(jti)
    return token is not None


if __name__ == "__main__":
    app.run(
            host=os.getenv('ETA_API_HOST', '0.0.0.0'),
            port=int(os.getenv('ETA_API_PORT', '5000')),
            threaded=True
            )
