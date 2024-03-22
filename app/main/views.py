#!/usr/bin/python3
"""
Module implements all the views of the app
"""
from flask import render_template, url_for
from . import main
import uuid
from app.forms.authforms import SignInForm, SignUpForm


@main.route('/', strict_slashes=False)
def index():
    return render_template('base.html')


@main.route('/home', strict_slashes=False)
def home():
    return render_template('main/home.html', page_header='Home')
