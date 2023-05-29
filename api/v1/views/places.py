#!/usr/bin/python3
'''Blueprint index file'''
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage
from flask import abort, request
from models.place import Place


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def place(city_id):
    '''retrieves the list of all Place objects of a city'''
    all_city = storage.all('City')
    city = "City.{}".format(city_id)
    if city in all_city:
        places = all_city[city].places
        p_list = [i.to_dict() for i in places]

        return jsonify(p_list)

    abort(404)


@app_views.route('/places/<string:place_id>', strict_slashes=False,
                 methods=['GET'])
def place_by_id(place_id):
    '''retreive a place by its id, raise 404 if id not found'''
    for key, value in storage.all('Place').items():
        p_id = key.split('.')[1]
        if place_id == p_id:
            return jsonify(value.to_dict())

    abort(404)


@app_views.route('/places/<string:place_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_place(place_id):
    '''Delete a place based on its id, raise 404 if id not found'''
    place = "Place.{}".format(place_id)
    for key, value in storage.all('Place').items():
        if place == key:
            storage.delete(value)
            storage.save()
            return make_response(jsonify({}), 200)

    abort(404)


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['POST'])
def create_place(city_id):
    '''create a new place object'''
    city_key = 'City.{}'.format(city_id)
    if city_key not in storage.all('City'):
        abort(404)

    if not request.get_json():
        reply = 'Not a JSON'
        return make_response(jsonify(reply), 400)

    place_dict = request.get_json()
    if 'user_id' not in place_dict:
        reply = 'Missing user_id'
        return make_response(jsonify(reply), 400)

    user_key = "User.{}".format(place_dict['user_id'])
    if user_key not in storage.all('User'):
        abort(404)

    if 'name' not in place_dict:
        reply = 'Missing name'
        return make_response(jsonify(reply), 400)

    instance = Place(city_id=city_id, **place_dict)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/places/<string:place_id>', strict_slashes=False,
                 methods=['PUT'])
def update_place(place_id):
    '''Update a state based on its id'''
    key = 'Place.{}'.format(place_id)
    if key not in storage.all('Place'):
        abort(404)

    if not request.get_json():
        reply = 'Not a JSON'
        return make_response(jsonify(reply), 400)

    obj = storage.all('Place')[key]

    ignore = ['id', 'user_id', 'city_id', 'created_at', 'updated_at']

    for key, value in request.get_json().items():
        if key in ignore:
            continue
        setattr(obj, key, value)
        obj.save()

    return make_response(jsonify(obj.to_dict()), 200)
