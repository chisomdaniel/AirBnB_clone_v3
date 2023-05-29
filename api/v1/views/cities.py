#!/usr/bin/python3
'''Blueprint index file'''
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage
from flask import abort, request
from models.city import City


@app_views.route('/cities/<string:city_id>', methods=['GET'],
                 strict_slashes=False)
def city_by_id(city_id):
    '''retrieves the list of all cities of a state'''
    all_city = storage.all('City')
    c_key = "City.{}".format(city_id)
    for key, value in all_city.items():
        if key == c_key:
            return jsonify(value.to_dict())

    abort(404)


@app_views.route('/states/<string:state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def city_by_state(state_id):
    '''retrieves the list of all cities of a state'''
    for key, value in storage.all('State').items():
        s_id = key.split('.')[1]
        if state_id == s_id:
            cities = value.cities
            c_list = [each.to_dict() for each in cities]
            return jsonify(c_list)

    abort(404)


@app_views.route('/cities/<string:city_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_city(city_id):
    '''Delete a city based on its id, raise 404 if id not found'''
    city = "City.{}".format(city_id)
    for key, value in storage.all('City').items():
        if city == key:
            storage.delete(value)
            storage.save()
            return make_response(jsonify({}), 200)

    abort(404)


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    '''create a new city object'''
    if not request.get_json():
        reply = 'Not a JSON'
        return make_response(jsonify(reply), 400)

    if 'name' not in request.get_json():
        reply = 'Missing name'
        return make_response(jsonify(reply), 400)

    state = "State.{}".format(state_id)
    if state not in storage.all('State').keys():
        abort(404)

    city_dict = request.get_json()
    instance = City(state_id=state_id, **city_dict)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/cities/<string:city_id>', strict_slashes=False,
                 methods=['PUT'])
def update_city(city_id):
    '''Update a city based on its id'''
    key = 'City.{}'.format(city_id)
    if key not in storage.all('City'):
        abort(404)

    if not request.get_json():
        reply = 'Not a JSON'
        return make_response(jsonify(reply), 400)

    obj = storage.all('City')[key]

    ignore = ['id', 'created_at', 'updated_at']

    for key, value in request.get_json().items():
        if key in ignore:
            continue
        setattr(obj, key, value)

    obj.save()
    return make_response(jsonify(obj.to_dict()), 200)
