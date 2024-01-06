#!/usr/bin/python3
from models import storage
from models.state import State
from flask import Flask, Blueprint, jsonify, abort, make_response
from api.v1.views import app_views

app_views.route('/states' , methods=['GET'], strict_slashes=False)
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