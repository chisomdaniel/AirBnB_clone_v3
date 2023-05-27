#!/usr/bin/python3
'''Blueprint index file'''
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models import Amenity, City, Pla

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
                "amenities": storage.count('')
            }
