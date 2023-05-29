#!/usr/bin/python3
'''Blueprint index file'''
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage
from flask import abort, request
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    '''retrieves the list of all Amenity objects'''
    all_amenity = storage.all('Amenity')
    a_list = [value.to_dict() for value in all_amenity.values()]

    return jsonify(a_list)


@app_views.route('/amenities/<string:amenity_id>', strict_slashes=False,
                 methods=['GET'])
def amenity_by_id(amenity_id):
    '''retreive an amenity by its id, raise 404 if id not found'''
    for key, value in storage.all('Amenity').items():
        a_id = key.split('.')[1]
        if amenity_id == a_id:
            return jsonify(value.to_dict())

    abort(404)


@app_views.route('/amenities/<string:amenity_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_amenity(amenity_id):
    '''Delete an amenity based on its id, raise 404 if id not found'''
    amenity = "Amenity.{}".format(amenity_id)
    for key, value in storage.all('Amenity').items():
        if amenity == key:
            storage.delete(value)
            storage.save()
            return make_response(jsonify({}), 200)

    abort(404)


@app_views.route('/amenities', strict_slashes=False, methods=['POST'])
def create_amenity():
    '''create a new amenity object'''
    if not request.get_json():
        reply = 'Not a JSON'
        return make_response(jsonify(reply), 400)

    if 'name' not in request.get_json():
        reply = 'Missing name'
        return make_response(jsonify(reply), 400)

    state_dict = request.get_json()
    instance = Amenity(**state_dict)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', strict_slashes=False,
                 methods=['PUT'])
def update_amenity(amenity_id):
    '''Update an amenity based on its id'''
    key = 'Amenity.{}'.format(amenity_id)
    if key not in storage.all('Amenity'):
        abort(404)

    if not request.get_json():
        reply = 'Not a JSON'
        return make_response(jsonify(reply), 400)

    obj = storage.all('Amenity')[key]

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in request.get_json().items():
        if key in ignore:
            continue
        setattr(obj, key, value)

    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
