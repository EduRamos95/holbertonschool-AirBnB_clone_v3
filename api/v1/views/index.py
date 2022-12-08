#!/usr/bin/python3
"""
Module index:
   url_prefix = '/api/v1'
   routes:
       - '/status'
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status')
def status():
    """status"""
    return jsonify({"status": "OK"})
