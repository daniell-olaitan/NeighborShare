#!/usr/bin/python3
"""
Module creates and initializes auth blueprint
"""
from flask import Blueprint

auth = Blueprint('auth', __name__)

from . import authviews
