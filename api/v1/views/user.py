#!/usr/bin/python3
"""User API"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/users/', methods=['GET'])
@app_views.route('/users', methods=['GET'])
def get_users():
    """Retrieves a list of all users"""
    users = storage.all(User)
    list_users = []
    for user in users.values():
        list_users.append(user.to_dict())
    return jsonify(list_users), 200


@app_views.route('/users/<string:u_id>', methods=['GET'])
def get_user(u_id):
    """Obtains single user"""
    valid_id = storage.get(User, u_id)
    if valid_id is None:
        abort(404)
    return jsonify(valid_id.to_dict())


@app_views.route('/users/<string:u_id>', methods=['DELETE'])
def delete_user(u_id):
    """Deletes a user"""
    valid_id = storage.get(User, u_id)
    if valid_id is None:
        abort(404)
    storage.delete(valid_id)
    storage.save()
    return {}, 200


@app_views.route('/users/', methods=['POST'])
@app_views.route('/users', methods=['POST'])
def create_user():
    """Creates new user"""
    if request.is_json:
        req = request.get_json()
        if req.get('email') is None:
            abort(400, description="Missing email")
        if req.get('password') is None:
            abort(400, description="Missing password")
        new_user = User(**req)
        storage.new(new_user)
        storage.save()
        return jsonify(new_user.to_dict()), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/users/<string:u_id>', methods=['PUT'])
def update_user(u_id):
    """Updates existing user"""
    valid_id = storage.get(User, u_id)
    if valid_id is None:
        abort(404)
    if request.is_json:
        req = request.get_json()
        ignore = ["id", "email", "created_at", "updated_at"]
        storage.delete(valid_id)
        for key, value in req.items():
            if key not in ignore:
                setattr(valid_id, key, value)
        storage.new(valid_id)
        storage.save()
        return jsonify(valid_id.to_dict()), 200

    else:
        abort(400, description="Not a JSON")
