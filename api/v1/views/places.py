#!/usr/bin/python3
"""define module places that handles all default RESTFul API actions"""
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import Flask, Blueprint, jsonify, abort, make_response, request
from api.v1.views import app_views


app = Flask(__name__)
app_views = Blueprint('app_views', __name__)


app_views.route('/cities/<city_id>/places',
                methods=['GET'], strict_slashes=False)


def get_places(city_id):
    """get all places object"""
    all_places = storage.all(Place).values()
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    new_list = []
    for place in all_places:
        for city in place.cities:
            if city.id == city_id:
                new_list.append(place.to_dict())
    return jsonify(new_list)


app_views.route('/places/<place_id>',
                methods=['GET'], strict_slashes=False)


def get_place_id(place_id):
    """get places by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


app_views.route('/places/<place_id>',
                methods=['DELETE'], strict_slashes=False)


def delete_place(place_id):
    """delete place from engine storage"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return make_response(jsonify({}), 200)


app_views.route('/cities/<city_id>/places',
                methods=['POST'], strict_slashes=False)


def create_place(city_id):
    """update places from engine storage"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)

    if not request.get_json():
        abort(400, description='Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, description='Missing user_id')
    if 'name' not in request.get_json():
        abort(400, description='Missing name')

    data = request.get_json()

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    data['city_id'] = city_id
    new_place = Place(**data)
    new_place.save()
    return make_response(jsonify(new_place.to_dict()), 201)


app_views.route('/places/<place_id>',
                methods=['PUT'], strict_slashes=False)


def update_place(place_id):
    """update place by id"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'created_at ', 'updated_at']
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(place, k, v)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)
