#!/usr/bin/python3
"""Places API"""
from models import storage
from models.place import Place
from models.user import User
from models.city import City
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/cities/<string:c_id>/places/', methods=['GET'])
@app_views.route('/cities/<string:c_id>/places', methods=['GET'])
def get_places(c_id):
    """Retrieves a list of all Place objects of a city"""
    valid_id = storage.get(City, c_id)
    if valid_id is None:
        abort(404)
    if valid_id.places is None:
        abort(404)
    place_list = []
    for place in valid_id.places:
        place_list.append(place.to_dict())
    return jsonify(place_list), 200


@app_views.route('/places/<string:p_id>', methods=['GET'])
def get_place(p_id):
    """Retrieves a place Id"""
    valid_id = storage.get(Place, p_id)
    if valid_id is None:
        abort(404)
    return jsonify(valid_id.to_dict()), 200


@app_views.route('/places/<string:p_id>', methods=['DELETE'])
def delete_place(p_id):
    """Deletes a Place"""
    valid_id = storage.get(Place, p_id)
    if valid_id is None:
        abort(404)
    storage.delete(valid_id)
    storage.save()
    return {}, 200


@app_views.route('/cities/<string:c_id>/places/', methods=['POST'])
@app_views.route('/cities/<string:c_id>/places', methods=['POST'])
def create_place(c_id):
    """Creates a place"""
    if request.is_json:
        valid_id = storage.get(City, c_id)
        if valid_id is None:
            abort(404)
        req = request.get_json()
        u_id = req.get('user_id')
        if u_id is None:
            abort(400, description="Missing user_id")
        valid_uid = storage.get(User, u_id)
        if valid_uid is None:
            abort(404)
        if req.get('name') is None:
            abort(400, description="Missing name")
        req['city_id'] = c_id
        new_place = Place(**req)
        storage.new(new_place)
        storage.save()
        return jsonify(new_place.to_dict()), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/places/<string:p_id>', methods=['PUT'])
def update_place(p_id):
    """Updates Place"""
    valid_id = storage.get(Place, p_id)
    if valid_id is None:
        abort(404)
    if request.is_json:
        req = request.get_json()
        ignore = ["id", "user_id", "city_id", "created_at", "updated_at"]
        storage.delete(valid_id)
        for key, value in req.items():
            if key not in ignore:
                setattr(valid_id, key, value)
        storage.new(valid_id)
        storage.save()
        return jsonify(valid_id.to_dict()), 200
    else:
        abort(400, description="Not a JSON")
