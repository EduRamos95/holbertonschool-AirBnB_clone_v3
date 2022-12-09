#!/usr/bin/python3
"""
Module cities
route:
    - route cities
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def cities_by_state(state_id=None):
    """ Retrieves the list of all City objects of a State """
    list_json = []
    if state_id is not None:
        if storage.get("State", state_id) is None:
            abort(404)
        else:
            for obj_city in storage.all("City").values():
                if obj_city.state_id == state_id:
                    list_json.append(obj_city.to_dict())
    return jsonify(list_json)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def cities_by_id(city_id=None):
    """ Retrieves a City object """
    if city_id is not None:
        obj_city_id = storage.get("City", city_id)
        if obj_city_id is not None:
            return jsonify(obj_city_id.to_dict())
        else:
            abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def cities_delete(city_id=None):
    """ Deletes a City object: DELETE """
    if city_id is None:
        abort(404)
    obj_city_id = storage.get("City", city_id)
    if obj_city_id is None:
        abort(404)
    storage.delete(obj_city_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def cities_create(state_id=None):
    """ Creates a City """
    dict_cities = {}
    if state_id is not None:
        if storage.get("State", state_id) is None:
            print(state_id)
            abort(404)
        else:
            if request.get_json() is None:
                abort(400, 'Not a JSON')
            if 'name' not in request.get_json():
                abort(400, 'Missing name')
            request.get_json()['state_id'] = state_id
            print(request.get_json())
            obj = storage.create("City", **request.get_json())
            storage.new(obj)
            storage.save()
            return jsonify(obj.to_dict()), 201
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_cities(city_id):
    """ Updates a City object """
    if city_id is None:
        abort(404)
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    print(request.get_json())
    obj_update = storage.update(city, **request.get_json())
    old_dict = obj_update.to_dict()
    storage.delete(city)
    obj_new = storage.create("City", **old_dict)
    obj_new.save()
    return jsonify(obj_new.to_dict()), 200
