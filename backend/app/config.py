#!/usr/bin/python3
"""
Configuration file for the project
"""
from os import getenv
from datetime import timedelta


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
    JWT_SECRET_KEY = getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=10)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=15)
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    FRONTEND_BASE_URL = 'http://localhost:5173'


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
