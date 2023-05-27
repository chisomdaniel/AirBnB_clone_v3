#!/usr/bin/python3
'''Blueprint index file'''
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def api_status():
    '''check to ensure our api is functioning well'''
    status = {
                "status": "OK"
            }
    return jsonify(status)


@app_views.route('/stats')
def check_stats():
    '''retrieves the number of object by type'''
    stats = {
                "amenities": storage.count('Amenity'),
                "cities": storage.count('City'),
                "places": storage.count('Place'),
                "reviews": storage.count('Review'),
                "states": storage.count('State'),
                "users": storage.count('User')
            }
    return jsonity(stats)
