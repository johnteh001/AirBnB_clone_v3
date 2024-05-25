#!/usr/bin/python3
"""Review Module"""
from models import storage
from models.review import Review
from models.user import User
from models.place import Place
from api.v1.views import app_views
from flask import jsonify, abort, request


@app_views.route('/places/<string:p_id>/reviews/', methods=['GET'])
@app_views.route('/places/<string:p_id>/reviews', methods=['GET'])
def get_reviews(p_id):
    """Retrieves all Reviews"""
    valid_id = storage.get(Place, p_id)
    if valid_id is None:
        abort(404)
    if valid_id.reviews is None:
        abort(404)
    list_review = []
    for review in valid_id.reviews:
        list_review.append(review.to_dict())
    return jsonify(list_review), 200


@app_views.route('/reviews/<string:r_id>', methods=['GET'])
def get_review(r_id):
    """Retrieve a review"""
    valid_id = storage.get(Review, r_id)
    if valid_id is None:
        abort(404)
    return jsonify(valid_id.to_dict()), 200


@app_views.route('/reviews/<string:r_id>', methods=['DELETE'])
def delete_review(r_id):
    """Deletes a Review"""
    valid_id = storage.get(Review, r_id)
    if valid_id is None:
        abort(404)
    storage.delete(valid_id)
    storage.save()
    return {}, 200


@app_views.route('/places/<string:p_id>/reviews/', methods=['POST'])
@app_views.route('/places/<string:p_id>/reviews', methods=['POST'])
def create_review(p_id):
    """Creates a new review"""
    if request.is_json:
        req = request.get_json()
        valid_id = storage.get(Place, p_id)
        if valid_id is None:
            abort(404)
        u_id = req.get('user_id')
        if u_id is None:
            abort(400, description="Missing user_id")
        valid_uid = storage.get(User, u_id)
        if valid_uid is None:
            abort(404)
        if req.get('text') is None:
            abort(400, description="Missing text")
        req['place_id'] = p_id
        new_review = Review(**req)
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201
    else:
        abort(400, description="Not a JSON")


@app_views.route('/reviews/<string:r_id>', methods=['PUT'])
def update_review(r_id):
    """Updates review"""
    if request.is_json:
        req = request.get_json()
        valid_id = storage.get(Review, r_id)
        if valid_id is None:
            abort(404)
        storage.delete(valid_id)
        ignore = ["id", "user_id", "place_id", "created_at", "updated_at"]
        for key, value in req.items():
            if key not in ignore:
                setattr(valid_id, key, value)
        storage.new(valid_id)
        storage.save()
        return jsonify(valid_id.to_dict()), 200
    else:
        abort(400, description="Not a JSON")
