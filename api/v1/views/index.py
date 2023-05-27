#!/usr/bin/python3
'''Blueprint index file'''
from api.v1.views import app_views
from flask import jsonify

@app_views.route('/status')
def api_status():
    '''check to ensure our api is functioning well'''
    status = {
                "status": "OK"
            }
    return jsonify(status)
