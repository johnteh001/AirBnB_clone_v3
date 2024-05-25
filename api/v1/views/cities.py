#!/usr/bin/python3
"""Cities API"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
import json
from models.city import City
from models.state import State


@app_views.route('/states/<string:state_id>/cities/', methods=['GET'])
@app_views.route('/states/<string:state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """Retrieves Cities of state"""
    valid_id = storage.get(State, state_id)
    if valid_id is None:
        abort(404)
    if valid_id.cities is None:
        abort(404)
    else:
        cities = valid_id.cities
        list_cities = []
        for city in cities:
            list_cities.append(city.to_dict())
        return (jsonify(list_cities))


@app_views.route('/cities/<string:city_id>', methods=['GET'])
def get_city(city_id, strict_slashes=False):
    """Retrieves specific city of given Id"""
    valid_id = storage.get(City, city_id)
    if valid_id is None:
        abort(404)
    return (jsonify(valid_id.to_dict()))


@app_views.route('/cities/<string:city_id>', methods=['DELETE'])
def delete_city(city_id, strict_slashes=False):
    """Deletes a city object of given Id"""
    valid_id = storage.get(City, city_id)
    if valid_id is None:
        abort(404)
    storage.delete(valid_id)
    storage.save()
    return {}, 200


@app_views.route('/states/<string:state_id>/cities/', methods=['POST'])
@app_views.route('/states/<string:state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Creates a new city object based on state Id"""
    valid_id = storage.get(State, state_id)
    if valid_id is None:
        abort(404)
    if request.is_json:
        req = request.get_json()
        if req.get("name") is None:
            abort(400, description="Missing name")
        else:
            req['state_id'] = state_id
            new_city = City(**req)
            storage.new(new_city)
            storage.save()
            return new_city.to_dict(), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/cities/<string:city_id>', methods=['PUT'])
def update_city(city_id, strict_slashes=False):
    """Updates an existing city of given Id"""
    valid_id = storage.get(City, city_id)
    if valid_id is None:
        abort(404)
    if request.is_json:
        req = request.get_json()
        ignore = ["id", "created_at", "updated_at"]
        storage.delete(valid_id)
        for key, value in req.items():
            if key not in ignore:
                setattr(valid_id, key, value)
        storage.new(valid_id)
        storage.save()
        return valid_id.to_dict(), 200
    else:
        abort(400, description="Not a JSON")
