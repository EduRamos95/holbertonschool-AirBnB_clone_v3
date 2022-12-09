#!/usr/bin/python3
"""
Module state
route:
    - route states
"""

from api.v1.views import app_views
from flask import abort, jsonify
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

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def states_delete(state_id=None):
    """delete object choose by id"""
    if state_id is None:
        abort(404)
    obj_state_id = storage.get("State", state_id)
    if obj_state_id is None:
        abort(404)
    storage.delete(obj_state_id)
    storage.save()
    return jsonify({})
