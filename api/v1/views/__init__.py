#!/usr/bin/python3
"""
Module __init__
    instance: app_views
"""
from api.v1.views.index import *
from flask import Blueprint

app_views = Blueprint(url_prefix='/api/v1')
