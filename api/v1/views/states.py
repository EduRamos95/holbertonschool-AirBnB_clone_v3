#!/usr/bin/python3
"""
Module state
route:
    - route states
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def states(state_id=None):
    """all object state"""
    list_json = []
    if state_id is not None:
        obj_state_id = storage.get("State", state_id)
        if obj_state_id is not None:
            list_json.append(obj_state_id.to_dict())
        else:
            abort(404)
    else:
        for obj in storage.all("State").values():
            list_json.append(obj.to_dict())
    return jsonify(list_json)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def states_delete(state_id=None):
    """delete object choose by id"""
    if state_id is None:
        abort(404)
    obj_state_id = storage.get("State", state_id)
    if obj_state_id is None:
        abort(404)
    storage.delete(obj_state_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def states_create():
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    obj = storage.create("State", **request.get_json())
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    if state_id is None:
        abort(404)
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    obj_update = storage.update(state, **request.get_json())
    # obj_update.save()
    old_dict = obj_update.to_dict()
    storage.delete(state)
    obj_new = storage.create("State", **old_dict)
    obj_new.save()
    # storage.new(obj_new)
    # storage.save()
    return jsonify(obj_new.to_dict()), 200
