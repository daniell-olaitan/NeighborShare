#!/usr/bin/python3
"""
Module creates and initializes main blueprint
"""
from flask import Blueprint

main = Blueprint('main', __name__)

from . import errors, views
