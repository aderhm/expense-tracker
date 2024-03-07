#!/usr/bin/python3
"""Contains the index routes.
"""

from api.v1.views import appi
from flask import jsonify, request
from flask_jwt_extended import (
        create_access_token,
        get_jwt_identity,
        get_jwt,
        get_jwt_identity,
        jwt_required,
        verify_jwt_in_request
        )
from hashlib import md5
from models import storage
from models.user import User
from models.token_block_list import TokenBlockList


@appi.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns status code.
    """
    return jsonify(status="OK")


@appi.route('/register', methods=['POST'], strict_slashes=False)
def register():
    """Registers a new user.
    """
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({
            'message': 'Username, email, and password are required.'
            }), 400

    existing_user = storage.check_account_existence(email)
    if existing_user:
        return jsonify({
            'message': 'User with this email already exists'
            }), 409

    new_user = User(username=username, email=email, password=password)
    storage.new(new_user)
    storage.save()

    access_token = create_access_token(identity=new_user.id)
    return jsonify({'access_token': access_token}), 201


@appi.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """Signs a user in.
    """
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = storage.check_account_existence(email)
    if not user or user.password != md5(password.encode()).hexdigest():
        return jsonify({'message': 'Invalid email or password'}), 401

    access_token = create_access_token(identity=user.id)
    return jsonify({'access_token': access_token}), 200


@appi.route('/logout', methods=['POST'], strict_slashes=False)
@jwt_required()
def logout():
    jti = get_jwt()['jti']
    token_blocklist = TokenBlockList(jti=jti)
    storage.new(token_blocklist)
    storage.save()
    return jsonify({'message': 'Successfully logged out'}), 200


@appi.route('/protected', methods=['GET'], strict_slashes=False)
@jwt_required()
def protected():
    return jsonify({'message': 'This is a protected endpoint'}), 200
