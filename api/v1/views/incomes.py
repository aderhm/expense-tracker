#!/usr/bin/python3
"""Contains the incomes routes.
"""
from api.v1.views import appi
from flask import abort, jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import storage
from models.income import Income


@appi.route('/incomes', methods=['GET'], strict_slashes=False)
@jwt_required()
def incomes():
    """Returns the list of all incomes.
    """
    current_user = get_jwt_identity()
    incs = storage.get_by_fk(Income, current_user)
    serialized_data = []
    for obj in incs:
        incomes_data = {
                "id": obj.id,
                "category": obj.category,
                "amount": obj.amount,
                "user_id": obj.user_id,
                "created_at": obj.created_at,
                "updated_at": obj.updated_at
                }
        serialized_data.append(incomes_data)
    return jsonify(serialized_data), 200


@appi.route('/income/<income_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def income(income_id):
    """Gets an income by id.
    """
    inc = storage.get(Income, income_id)
    if not inc:
        abort(404)
    income_data = [{
            "id": inc.id,
            "category": inc.category,
            "amount": inc.amount,
            "user_id": inc.user_id,
            "created_at": inc.created_at,
            "updated_at": inc.updated_at
            }]
    return make_response(jsonify(income_data), 200)


@appi.route('/income', methods=['POST'], strict_slashes=False)
@jwt_required()
def post_income():
    """Creates a new income.
    """
    data = request.json
    category = data.get('category')
    amount = data.get('amount')

    user_id = get_jwt_identity()

    if not category or not amount:
        return jsonify({
            "message": "Category and amount are required!"
        }), 400
    
    new_income = Income(
        category=category,
        amount=amount,
        user_id=user_id
        )
    storage.new(new_income)
    storage.save()

    new_income_data = [{
            "id": new_income.id,
            "category": new_income.category,
            "amount": new_income.amount,
            "user_id": new_income.user_id,
            "created_at": new_income.created_at,
            "updated_at": new_income.updated_at
            }]

    return make_response(jsonify(new_income_data), 201)


@appi.route('/income/<income_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def put_income(income_id):
    """Updates an income.
    """

    inc = storage.get(Income, income_id)
    if not inc:
        abort(404)

    data = request.json
    if not data:
        abort(400, "Not a JSON")
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(inc, k, v)

    storage.save()
    updated_income_data = [{
            "id": inc.id,
            "category": inc.category,
            "amount": inc.amount,
            "user_id": inc.user_id,
            "created_at": inc.created_at,
            "updated_at": inc.updated_at
            }]

    return make_response(jsonify(updated_income_data), 200)


@appi.route('/income/<income_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def del_income(income_id):
    """Deletes an income.
    """
    inc = storage.get(Income, income_id)
    if not inc:
        abort(404)
    inc.delete()
    storage.save()
    return make_response(jsonify({}), 200)
