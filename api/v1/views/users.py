#!/usr/bin/python3
"""
Module user
route:
    - /users           : GET , POST
    - /users/<user_id> : GET , DELETE, PUT
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def users(user_id=None):
    """ all object user """
    list_json = []
    var_id = user_id
    var_cls = "User"
    if var_id is not None:
        obj = storage.get(var_cls, var_id)
        if obj is not None:
            return jsonify(obj.to_dict())
        else:
            abort(404)
    else:
        for obj in storage.all(var_cls).values():
            list_json.append(obj.to_dict())
    return jsonify(list_json)


@app_views.route('/users/<user_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def users_delete(user_id=None):
    """ delete object choose by id """
    var_id = user_id
    var_cls = "User"
    if var_id is None:
        abort(404)
    obj = storage.get(var_cls, var_id)
    if obj is None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def users_create():
    """ Creates a User """
    var_cls = "User"
    var_dict = request.get_json()
    if var_dict is None:
        abort(400, 'Not a JSON')
    if 'email' not in var_dict.keys():
        abort(400, 'Missing email')
    if 'password' not in var_dict.keys():
        abort(400, 'Missing password')
    obj = storage.create(var_cls, **var_dict)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """ Updates a User object """
    var_id = user_id
    var_cls = "User"
    var_dict = request.get_json()
    if var_id is None:
        abort(404)
    obj = storage.get(var_cls, var_id)
    if obj is None:
        abort(404)
    if var_dict is None:
        abort(400, 'Not a JSON')
    obj_update = storage.update(obj, **var_dict)
    update_dict = obj_update.to_dict()
    storage.delete(obj)
    obj_new = storage.create(var_cls, **update_dict)
    obj_new.save()
    # storage.new(obj_new)
    # storage.save()
    return jsonify(obj_new.to_dict()), 200
