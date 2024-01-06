#!/usr/bin/python3
from models import storage
from models.state import State
from flask import Flask, Blueprint, jsonify, abort, make_response, request
from api.v1.views import app_views


app_views.route('/states', methods=['GET'], strict_slashes=False)


def get_states():
    all_states = storage.all(State).values()
    new_list = []
    for state in all_states:
        new_list.append(state.to_dict())
    return jsonify(new_list)


app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)


def get_state_id(state_id):
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)


def delete_state(state_id):
    state = storage.get(State, state)
    if not state:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


app_views.route('/states', methods=['POST'], strict_slashes=False)


def create_state():
    if not request.get_json():
        abort(400, description='Not a JSON')
    if 'name' not in request.get_json():
        abort(400, description='Missing name')
    data = request.get_json()
    new_state = State(**data)
    new_state.save()
    return make_response(jsonify(new_state.to_dict()), 201)


app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)


def update_state(state_id):
    state = storage.get(State, state)
    if not state:
        abort(404)
    if not request.get_json():
        abort(400, description='Not a JSON')
    data = request.get_json()
    ignore_keys = ['id', 'created_at ', 'updated_at']
    for k, v in data.items():
        if k not in ignore_keys:
            setattr(state, k, v)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
