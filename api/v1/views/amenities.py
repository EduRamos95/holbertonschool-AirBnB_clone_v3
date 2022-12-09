#!/usr/bin/python3
"""
Module Amenities
route:
    - route amenity
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
@app_views.route('/amenities/<amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenities_get(amenity_id=None):
    """ Retrieves the list of all Amenity objects """
    list_json = []
    if amenity_id is not None:
        obj_amenity_id = storage.get("Amenity", amenity_id)
        if obj_amenity_id is not None:
            return jsonify(obj_amenity_id.to_dict())
        else:
            abort(404)
    else:
        for obj in storage.all("Amenity").values():
            list_json.append(obj.to_dict())
    return jsonify(list_json)


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def amenity_delete(amenity_id=None):
    """ Deletes a Amenity object """
    if amenity_id is None:
        abort(404)
    obj_amenity_id = storage.get("Amenity", amenity_id)
    if obj_amenity_id is None:
        abort(404)
    storage.delete(obj_amenity_id)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenity_create():
    """ Creates a Amenity """
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    obj = storage.create("Amenity", **request.get_json())
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def amenity_update(amenity_id):
    """ Updates a Amenity object """
    if amenity_id is None:
        abort(404)
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if request.get_json() is None:
        abort(400, 'Not a JSON')
    obj_update = storage.update(amenity, **request.get_json())
    old_dict = obj_update.to_dict()
    storage.delete(amenity)
    obj_new = storage.create("Amenity", **old_dict)
    obj_new.save()
    return jsonify(obj_new.to_dict()), 200
