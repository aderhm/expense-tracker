#!/usr/bin/python3
"""Contains the Blueprint for the API.
"""

from flask import Blueprint

appi = Blueprint('appi', __name__, url_prefix="/api/v1")

from api.v1.views.index import *
