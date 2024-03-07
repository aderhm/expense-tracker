#!/usr/bin/python3
"""Contains the expenses routes.
"""
from api.v1.views import appi
from flask import abort, jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import storage
from models.expense import Expense


@appi.route('/expenses', methods=['GET'], strict_slashes=False)
@jwt_required()
def expenses():
    """Returns the list of all expenses.
    """
    current_user = get_jwt_identity()
    exps = storage.get_by_fk(Expense, current_user)
    serialized_data = []
    for obj in exps:
        expenses_data = {
                "id": obj.id,
                "category": obj.category,
                "description": obj.description,
                "amount": obj.amount,
                "user_id": obj.user_id,
                "created_at": obj.created_at,
                "updated_at": obj.updated_at
                }
        serialized_data.append(expenses_data)
    return jsonify(serialized_data), 200


@appi.route('/expense/<expense_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def expense(expense_id):
    """Gets an expense by id.
    """
    exp = storage.get(Expense, expense_id)
    if not exp:
        abort(404)
    expense_data = [{
            "id": exp.id,
            "category": exp.category,
            "description": exp.description,
            "amount": exp.amount,
            "user_id": exp.user_id,
            "created_at": exp.created_at,
            "updated_at": exp.updated_at
            }]
    return make_response(jsonify(expense_data), 200)


@appi.route('/expense', methods=['POST'], strict_slashes=False)
@jwt_required()
def post_expense():
    """Creates a new expense.
    """
    data = request.json
    category = data.get('category')
    amount = data.get('amount')

    if data.get('description'):
        description = data.get('description')
    else:
        description = None
    user_id = get_jwt_identity()

    if not category or not amount:
        return jsonify({
            "message": "Category and amount are required!"
        }), 400

    new_expense = Expense(
        category=category,
        description=description,
        amount=amount,
        user_id=user_id
        )
    storage.new(new_expense)
    storage.save()

    new_expense_data = [{
            "id": new_expense.id,
            "category": new_expense.category,
            "description": new_expense.description,
            "amount": new_expense.amount,
            "user_id": new_expense.user_id,
            "created_at": new_expense.created_at,
            "updated_at": new_expense.updated_at
            }]

    return make_response(jsonify(new_expense_data), 201)


@appi.route('/expense/<expense_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def put_expense(expense_id):
    """Updates an expense.
    """

    exp = storage.get(Expense, expense_id)
    if not exp:
        abort(404)

    data = request.json
    if not data:
        abort(400, "Not a JSON")
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(exp, k, v)

    storage.save()
    updated_expense_data = [{
            "id": exp.id,
            "category": exp.category,
            "description": exp.description,
            "amount": exp.amount,
            "user_id": exp.user_id,
            "created_at": exp.created_at,
            "updated_at": exp.updated_at
            }]

    return make_response(jsonify(updated_expense_data), 200)


@appi.route('/expense/<expense_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def del_expense(expense_id):
    """Deletes an expense.
    """
    exp = storage.get(Expense, expense_id)
    if not exp:
        abort(404)
    exp.delete()
    storage.save()
    return make_response(jsonify({}), 200)
