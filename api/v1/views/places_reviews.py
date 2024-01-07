#!/usr/bin/python3
"""define module places_reviews.py
that handles all default RESTFul API actions"""
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from models.review import Review
from flask import Flask, Blueprint, jsonify, abort, make_response, request
from api.v1.views import app_views


app = Flask(__name__)
app_views = Blueprint('app_views', __name__)


@app_views.route('/places/<place_id>/reviews',
                methods=['GET'], strict_slashes=False)
def get_reviews(place_id):
    """get all places_reviews.py object"""
    all_reviews = storage.all(Review).values()
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    new_list = []
    for place in all_reviews:
        for place in place.cities:
            if place.id == place_id:
                new_list.append(place.to_dict())
    return jsonify(new_list)


@app_views.route('/reviews/<review_id>',
                methods=['GET'], strict_slashes=False)
def get_review_id(review_id):
    """get places_reviews.py by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/reviews/<review_id>',
                methods=['DELETE'], strict_slashes=False)
def delete_review(review_id):
    """delete places_reviews.py from engine storage"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    storage.delete(review)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/places/<place_id>/reviews',
                methods=['POST'], strict_slashes=False)
def create_place_review(place_id):
    """update places_reviews.py from engine storage"""
    review = storage.get(Review, place_id)
    if not review:
        abort(404)

    if not request.get_json():
        abort(400, description='Not a JSON')
    if 'user_id' not in request.get_json():
        abort(400, description='Missing user_id')
    if 'name' not in request.get_json():
        abort(400, description='Missing name')
    if 'text' not in request.get_json():
        abort(400, description='Missing text')

    data = request.get_json()
    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    data['place_id'] = place_id
    new_review = Place(**data)
    new_review.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>',
                methods=['PUT'], strict_slashes=False)
def update_place_review(review_id):
    """update places_reviews.py by id"""
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'created_at ', 'updated_at',
                   'user_id', 'place_id']
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(review, k, v)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
