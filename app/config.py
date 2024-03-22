#!/usr/bin/python3
"""
Configuration file for the project
"""
from os import getenv
# from uuid import uuid4


class Config:
    """
    Class defines the common configurations of the project
    """
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = getenv('MAIL_USERNAME')
    MAIL_PASSWORD = getenv('MAIL_PASSWORD')
    MAIL_SENDER = getenv('MAIL_SENDER')


class DevelopmentConfig(Config):
    """
    Class defines the configurations that are specific to development
    """
    SQLALCHEMY_DATABASE_URI = "mysql://{}:{}@localhost/{}".format(
        getenv('DEV_DATABASE_USERNAME'),
        getenv('DEV_DATABASE_PASSWORD'),
        getenv('DEV_DATABASE'))


class ProductionConfig(Config):
    """
    Class defines the configurations that are specific to production
    """
    pass


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
