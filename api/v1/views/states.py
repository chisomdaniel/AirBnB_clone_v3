#!/usr/bin/python3
'''Blueprint index file'''
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage
from flask import abort, request
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    '''retrieves the list of all State objects'''
    all_state = storage.all('State')
    s_list = [value.to_dict() for value in all_state.values()]

    return jsonify(s_list)


@app_views.route('/states/<string:state_id>', strict_slashes=False, methods=['GET'])
def state_by_id(state_id):
    '''retreive a state by its id, raise 404 if id not found'''
    for key, value in storage.all('State').items():
        s_id = key.split('.')[1]
        if state_id == s_id:
            return jsonify(value.to_dict())

    abort(404)


@app_views.route('/states/<string:state_id>', strict_slashes=False, methods=['DELETE'])
def delete_state(state_id):
    '''Delete a state based on its id, raise 404 if id not found'''
    for key, value in storage.all('State').items():
        if state_id in key:
            storage.delete(value)
            return make_response(jsonify({}), 200)

    abort(404)


@app_views.route('/states/<string:state_id>', strict_slashes=False, methods=['POST'])
def create_state(state_id):
    '''create a new state object'''
    if not request.json:
        reply = 'Not a JSON'
        return make_response(jsonify(reply), 400)

    if 'name' not in request.json:
        reply = 'Missing name'
        return make_response(jsonify(reply), 400)

    state_dict = request.json
    instance = State(**state_dict)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/states/<string:state_id>', strict_slashes=False, methods=['PUT'])
def update_state(state_id):
    '''Update a state based on its id'''
    key = 'State.{}'.format(state_id)
    if key not in storage.all('State'):
        abort(404)
    if not request.get_json:
        reply = 'Not a JSON'
        return make_response(jsonify(reply), 400)

    obj = storage.all('State')[key]

    ignore = ['id', 'created_at', 'updated_at']
    for key, value in request.get_json:
        if key in ignore:
            continue

        setattr(obj, key, value)

    obj.save()
    return make_response(jsonify(obj.to_dict), 200)
