#!/usr/bin/python3
"""Contains the goals routes.
"""
from api.v1.views import appi
from flask import abort, jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models import storage
from models.goal import Goal


@appi.route('/goals', methods=['GET'], strict_slashes=False)
@jwt_required()
def goals():
    """Returns the list of all goals.
    """
    current_user = get_jwt_identity()
    gls = storage.get_by_fk(Goal, current_user)
    serialized_data = []
    for obj in gls:
        goals_data = {
                "id": obj.id,
                "purpose": obj.purpose,
                "target_amount": obj.target_amount,
                "monthly_saving_amount": obj.monthly_saving_amount,
                "deadline": obj.deadline,
                "user_id": obj.user_id,
                "created_at": obj.created_at,
                "updated_at": obj.updated_at
                }
        serialized_data.append(goals_data)
    return jsonify(serialized_data), 200


@appi.route('/goal/<goal_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def goal(goal_id):
    """Gets an goal by id.
    """
    gl = storage.get(Goal, goal_id)
    if not gl:
        abort(404)
    goal_data = [{
            "id": gl.id,
            "purpose": gl.purpose,
            "target_amount": gl.target_amount,
            "monthly_saving_amount": gl.monthly_saving_amount,
            "deadline": gl.deadline,
            "user_id": gl.user_id,
            "created_at": gl.created_at,
            "updated_at": gl.updated_at
            }]
    return make_response(jsonify(goal_data), 200)


@appi.route('/goal', methods=['POST'], strict_slashes=False)
@jwt_required()
def post_goal():
    """Creates a new goal.
    """
    data = request.json
    purpose = data.get('purpose')
    target_amount = data.get('target_amount')
    monthly_saving_amount = data.get('monthly_saving_amount')
    deadline = data.get('deadline')

    user_id = get_jwt_identity()

    if not purpose or not target_amount or (not monthly_saving_amount and not deadline):
        return jsonify({
            "message": "Purpose, target amount, \
                and monthly_saving_amount or deadline are required!"
        }), 400

    new_goal = Goal(
        purpose=purpose,
        target_amount=target_amount,
        monthly_saving_amount=monthly_saving_amount,
        deadline=deadline,
        user_id=user_id
        )
    storage.new(new_goal)
    storage.save()

    new_goal_data = [{
            "id": new_goal.id,
            "purpose": new_goal.purpose,
            "target_amount": new_goal.target_amount,
            "monthly_saving_amount": new_goal.monthly_saving_amount,
            "deadline": new_goal.deadline,
            "user_id": new_goal.user_id,
            "created_at": new_goal.created_at,
            "updated_at": new_goal.updated_at
            }]

    return make_response(jsonify(new_goal_data), 201)


@appi.route('/goal/<goal_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def put_goal(goal_id):
    """Updates an goal.
    """

    gl = storage.get(Goal, goal_id)
    if not gl:
        abort(404)

    data = request.json
    if not data:
        abort(400, "Not a JSON")
    for k, v in data.items():
        if k not in ['id', 'created_at', 'updated_at']:
            setattr(gl, k, v)

    storage.save()
    updated_goal_data = [{
            "id": gl.id,
            "purpose": gl.purpose,
            "target_amount": gl.target_amount,
            "monthly_saving_amount": gl.monthly_saving_amount,
            "deadline": gl.deadline,
            "user_id": gl.user_id,
            "created_at": gl.created_at,
            "updated_at": gl.updated_at
            }]

    return make_response(jsonify(updated_goal_data), 200)


@appi.route('/goal/<goal_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def del_goal(goal_id):
    """Deletes an goal.
    """
    gl = storage.get(Goal, goal_id)
    if not gl:
        abort(404)
    gl.delete()
    storage.save()
    return make_response(jsonify({}), 200)
