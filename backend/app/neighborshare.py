#!/usr/bin/python3
"""
Module creates and runs an instance of the app
"""
from os import getenv
from app import create_app

app = create_app(getenv('CONFIG') or 'default')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
