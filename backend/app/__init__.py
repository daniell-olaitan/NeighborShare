#!/usr/bin/python3
"""
Init file for the app
"""
from flask import Flask
from flask_mail import Mail
from app.config import config
from apscheduler.schedulers.background import BackgroundScheduler
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
import atexit

migrate = Migrate()
mail = Mail()
jwt = JWTManager()
scheduler = BackgroundScheduler()
scheduler.start()
atexit.register(lambda: scheduler.shutdown())


def create_app(config_name):
    """Creates an instance of the app and initialize
    the app and the extensions and registers the blueprints

    Args:
        config -> str:
            The name of the configuration to use

    Return: the created app instance
    """
    app = Flask(__name__)
    app.url_map.strict_slashes = False
    app.config.from_object(config[config_name])
    from .main import main as main_blueprint
    from .auth import auth as auth_blueprint
    app.register_blueprint(main_blueprint)
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    mail.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    jwt.init_app(app)
    with app.app_context():
        db.create_all()

    return app
