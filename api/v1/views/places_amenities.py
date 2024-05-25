#!/usr/bin/python3
"""Place_Amenity Module"""
from models import storage
from api.v1.views import app_views
from flask import jsonify, abort, request
from models.place import Place
from models.amenity import Amenity


@app_views.route('/places/<string:p_id>/amenities', methods=['GET'])
def get_amen(p_id):
    """Retrieves Amenity"""
    valid_id = storage.get(Place, p_id)
    if valid_id is None:
        abort(404)
    if valid_id.amenities is None:
        abort(404)
    amenities = valid_id.amenities
    list_amenities = []
    for amenity in amenities:
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities), 200


@app_views.route('/places/<string:p_id>/amenities/<string:am_id>',
                 methods=['DELETE'])
def delete_amen(p_id, am_id):
    """Deletes place_amenity"""
    valid_pid = storage.get(Place, p_id)
    if valid_pid is None:
        abort(404)
    valid_amid = storage.get(Amenity, am_id)
    if valid_amid is None:
        abort(404)
    if valid_amid.places is None:
        abort(404)
    storage.delete(valid_amid.places)
    storage.save()
    return {}, 200

@app_views.route('places/<string:p_id>/amenities/<string:am_id>',
                 methods=['POST'])
def create_amen(p_id, am_id):
    """Creates amenity"""
    valid_pid = storage.get(Place, p_id)
    if valid_pid is None:
        abort(404)
    valid_amid = storage.get(Amenity, am_id)
    if valid_amid is None:
        abort(404)
    if valid_amid.places:
        return jsonify(valid_amid.to_dict()), 200
    else:
        valid_amid['place_id'] = p_id
        new_amenity = Amenity(**valid_amid)
        storage.new(new_amenity)
        storage.save()
        return jsonify(new_amenity.to_dict()), 201
