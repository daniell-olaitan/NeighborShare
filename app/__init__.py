#!/usr/bin/python3
"""
Init file for the app
"""
from flask import Flask
from flask_login import LoginManager
from flask_mail import Mail
from config import config
from flask_migrate import Migrate
from flask_simple_geoip import SimpleGeoIP
from models import db

simple_geoip = SimpleGeoIP()
migrate = Migrate()
mail = Mail()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'


def create_app(config_name):
    """Creates an instance of the app and initialize
    the app and the extensions and registers the blueprints

    Args:
        config -> str:
            The name of the configuration to use

    Return: the created app instance
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    login_manager.init_app(app)
    mail.init_app(app)
    db.init_app(app)
    simple_geoip.init_app(app)
    migrate.init_app(app, db)
    with app.app_context():
        db.create_all()

    return app
