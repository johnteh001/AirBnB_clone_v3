#!/usr/bin/python3
"""index module"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.amenity import Amenity
from models.city import City
from models.review import Review
from models.place import Place
from models.state import State
from models.user import User

classes = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status')
def state():
    """Json status"""
    message = {"status": "OK"}
    return jsonify(message)


@app_views.route('/stats')
def numb_objects():
    """Retrieves the number of each objects by type"""
    objects = {}
    for obj in classes:
        objects[obj] = storage.count(classes[obj])
    return (jsonify(objects))
