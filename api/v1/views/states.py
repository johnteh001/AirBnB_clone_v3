#!/usr/bin/python3
"""State API"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
import json
from models.state import State


@app_views.route('/states/', methods=["GET"])
@app_views.route('/states', methods=["GET"])
def all_states():
    """Retrieves all state objects"""
    states = storage.all(State)
    states_list = []
    for state in states.values():
        states_list.append(state.to_dict())
    return jsonify(states_list)


@app_views.route('/states/<string:state_id>', methods=['GET'])
def get_state(state_id):
    """Retrieves a state of a given id"""
    validate_id = storage.get(State, state_id)
    if validate_id is None:
        abort(404)
    return (jsonify(validate_id.to_dict()))


@app_views.route('/states/<string:state_id>', methods=['DELETE'])
def delete_state(state_id):
    """Deletes a state of given id"""
    validate_id = storage.get(State, state_id)
    if validate_id is None:
        abort(404)
    storage.delete(validate_id)
    storage.save()
    return jsonify('{}'), 200


@app_views.route('/states', strict_slashes=False, methods=['POST'])
def create_state():
    """Creates a new state object"""
    if request.is_json:
        state = request.get_json()
        if state.get('name') is None:
            abort(400, description="Missing name")
        else:
            new_state = State(**state)
            state_id = new_state.id
            storage.new(new_state)
            storage.save()
            return new_state.to_dict(), 201
    else:
        abort(400, description='Not a Json')


@app_views.route('/states/<string:state_id>', methods=['PUT'])
def update_state(state_id):
    """Updates State object of given Id"""
    validate_id = storage.get(State, state_id)
    if validate_id is None:
        abort(404)
    if request.is_json:
        ignore = ["id", "created_at", "updated_at"]
        state = request.get_json()
        storage.delete(validate_id)
        for key, value in state.items():
            if state[key] not in ignore:
                setattr(validate_id, key, value)
        storage.new(validate_id)
        storage.save()
        return validate_id.to_dict(), 200
    else:
        abort(400, description="Not a JSON")
