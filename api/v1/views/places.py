#!/usr/bin/python3
"""
Module Place
route:
    - /cities/<city_id>/places:
          (GET, POST)
    - /places/<place_id>:
          (GET, DELETE, PUT)
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'],
                 strict_slashes=False)
def places_all_city(city_id=None):
    """ all places in city """
    list_json = []
    var_param = "city_id"
    var_rel_id = city_id
    var_rel_cls = "City"
    var_cls = "Place"

    if var_rel_id is None:
        abort(404)
    # verified existing City
    if var_rel_id is not None:
        obj_ver = storage.get(var_rel_cls, var_rel_id)
        if obj_ver is None:
            abort(404)
    # get all places in City
    for obj in storage.all(var_cls).values():
        if obj.__dict__.get(var_param, None) == var_rel_id:
            list_json.append(obj.to_dict())
    return jsonify(list_json)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def places_id(place_id=None):
    """ one specific place"""
    var_id = place_id
    var_cls = "Place"
    if var_id is None:
        abort(404)
    else:
        obj = storage.get(var_cls, var_id)
        if obj is not None:
            return jsonify(obj.to_dict())
        else:
            abort(404)
    return jsonify({"error": "fail"})


@app_views.route('/places/<place_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def place_delete(place_id=None):
    """ delete object choose by id """
    var_id = place_id
    var_cls = "Place"
    if var_id is None:
        abort(404)
    obj = storage.get(var_cls, var_id)
    if obj is not None:
        abort(404)
    storage.delete(obj)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def place_create(city_id=None):
    """ Creates a Place """
    var_param2 = "user_id"
    var_rel_cls2 = "User"
    var_rel_id = city_id
    var_rel_cls = "City"
    var_param = "city_id"
    var_cls = "Place"
    var_dict = request.get_json()

    # verify city
    obj = storage.get(var_rel_cls, var_rel_id)
    if obj is None:
        abort(404)

    if var_dict is None:
        abort(400, 'Not a JSON')

    # verify city_id in dict
    var_dict.update({var_param: var_rel_id})

    if 'user_id' not in var_dict.keys():
        abort(400, 'Missing user_id')

    # verify user
    obj = storage.get(var_rel_cls2, var_dict.get(var_param2, None))
    if obj is None:
        abort(404)

    if 'name' not in var_dict.keys():
        abort(400, 'Missing name')
    obj = storage.create(var_cls, **var_dict)
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'], strict_slashes=False)
def update_place(place_id=None):
    """ Updates a Place object """
    var_id = place_id
    var_cls = "Place"
    var_dict = request.get_json()
    if var_id is None:
        abort(404)
    # verify place
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
