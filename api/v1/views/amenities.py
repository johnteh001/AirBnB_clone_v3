#!/usr/bin/python3
"""Amenity API"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.amenity import Amenity


@app_views.route('/amenities/', methods=['GET'])
@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """Retrieves all the amenities objecs"""
    amenities = storage.all(Amenity).values()
    list_amenities = []
    for amenity in amenities:
        list_amenities.append(amenity.to_dict())
    return (jsonify(list_amenities)), 200


@app_views.route('/amenities/<string:am_id>/', methods=['GET'])
@app_views.route('/amenities/<string:am_id>', methods=['GET'])
def get_amenity(am_id):
    """Retrieves a given amenity"""
    valid_id = storage.get(Amenity, am_id)
    if valid_id is None:
        abort(404)
    return (jsonify(valid_id.to_dict())), 200


@app_views.route('/amenities/<string:am_id>', methods=['DELETE'])
def delete_amenity(am_id):
    """Deletes an amenity for a given Id"""
    valid_id = storage.get(Amenity, am_id)
    if valid_id is None:
        abort(404)
    storage.delete(valid_id)
    storage.save()
    return {}, 200


@app_views.route('/amenities/', methods=['POST'])
@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Creates an amenity"""
    if request.is_json:
        req = request.get_json()
        if req.get("name") is None:
            abort(400, description="Missing name")
        new_amenity = Amenity(**req)
        storage.new(new_amenity)
        storage.save()
        return (new_amenity.to_dict()), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/amenities/<string:am_id>', methods=['PUT'])
def update_amenity(am_id):
    """Updates the amenity based on Id"""
    valid_id = storage.get(Amenity, am_id)
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
        return (valid_id.to_dict()), 200
    else:
        abort(400, description="Not a JSON")
