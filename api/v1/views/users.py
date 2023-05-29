#!/usr/bin/python3
'''Blueprint index file'''
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage
from flask import abort, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    '''retrieves the list of all User objects'''
    all_user = storage.all('User')
    u_list = [value.to_dict() for value in all_user.values()]

    return jsonify(u_list)


@app_views.route('/users/<string:user_id>', strict_slashes=False,
                 methods=['GET'])
def user_by_id(user_id):
    '''retreive a user by its id, raise 404 if id not found'''
    for key, value in storage.all('User').items():
        u_id = key.split('.')[1]
        if user_id == u_id:
            return jsonify(value.to_dict())

    abort(404)


@app_views.route('/users/<string:user_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_user(user_id):
    '''Delete a user based on its id, raise 404 if id not found'''
    user = "User.{}".format(user_id)
    for key, value in storage.all('User').items():
        if user == key:
            storage.delete(value)
            storage.save()
            return make_response(jsonify({}), 200)

    abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    '''create a new user object'''
    if not request.get_json():
        reply = 'Not a JSON'
        return make_response(jsonify(reply), 400)

    user_dict = request.get_json()
    if 'email' not in user_dict:
        reply = 'Missing email'
        return make_response(jsonify(reply), 400)

    if 'password' not in user_dict:
        reply = 'Missing password'
        return make_response(jsonify(reply), 400)

    instance = User(**user_dict)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/users/<string:user_id>', strict_slashes=False,
                 methods=['PUT'])
def update_user(user_id):
    '''Update a User based on its id'''
    key = 'User.{}'.format(user_id)
    if key not in storage.all('User'):
        abort(404)

    if not request.get_json():
        reply = 'Not a JSON'
        return make_response(jsonify(reply), 400)

    obj = storage.all('User')[key]

    ignore = ['id', 'email', 'created_at', 'updated_at']

    for key, value in request.get_json().items():
        if key in ignore:
            continue
        setattr(obj, key, value)
        obj.save()

    return make_response(jsonify(obj.to_dict()), 200)
