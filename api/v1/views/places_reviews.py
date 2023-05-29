#!/usr/bin/python3
'''Blueprint index file'''
from api.v1.views import app_views
from flask import jsonify, make_response
from models import storage
from flask import abort, request
from models.review import Review


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def reviews(place_id):
    '''retrieves the list of all review objects of a place'''
    all_place = storage.all('Place')
    place_key = "Place.{}".format(place_id)
    if place_key in all_place:
        reviews = all_place[place_key].reviews
        r_list = [i.to_dict() for i in reviews]

        return jsonify(r_list)

    abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET'])
def review_by_id(review_id):
    '''retreive a review by its id, raise 404 if id not found'''
    for key, value in storage.all('Review').items():
        r_id = key.split('.')[1]
        if review_id == r_id:
            return jsonify(value.to_dict())

    abort(404)


@app_views.route('/reviews/<string:review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    '''Delete a place based on its id, raise 404 if id not found'''
    review = "Review.{}".format(review_id)
    for key, value in storage.all('Review').items():
        if review == key:
            storage.delete(value)
            storage.save()
            return make_response(jsonify({}), 200)

    abort(404)


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(place_id):
    '''create a new review object'''
    place_key = 'Place.{}'.format(place_id)
    if place_key not in storage.all('Place'):
        abort(404)

    if not request.get_json():
        reply = 'Not a JSON'
        return make_response(jsonify(reply), 400)

    review_dict = request.get_json()
    if 'user_id' not in review_dict:
        reply = 'Missing user_id'
        return make_response(jsonify(reply), 400)

    user_key = "User.{}".format(review_dict['user_id'])
    if user_key not in storage.all('User'):
        abort(404)

    if 'text' not in review_dict:
        reply = 'Missing text'
        return make_response(jsonify(reply), 400)

    instance = Review(place_id=place_id, **review_dict)
    instance.save()

    return make_response(jsonify(instance.to_dict()), 201)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['PUT'])
def update_review(review_id):
    '''Update a review based on its id'''
    key = 'Review.{}'.format(review_id)
    if key not in storage.all('Review'):
        abort(404)

    if not request.get_json():
        reply = 'Not a JSON'
        return make_response(jsonify(reply), 400)

    obj = storage.all('Review')[key]

    ignore = ['id', 'user_id', 'place_id', 'created_at', 'updated_at']

    for key, value in request.get_json().items():
        if key in ignore:
            continue
        setattr(obj, key, value)
        obj.save()

    return make_response(jsonify(obj.to_dict()), 200)
