#!/usr/bin/python3
"""
Module defines the User model
"""
from models.base_model import BaseModel
from models import db
from itsdangerous import TimedSerializer as Serializer
from flask import current_app, render_template
from flask_mail import Message
from hashlib import md5
from app import mail, scheduler
from datetime import datetime, timedelta
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import get_jwt_identity, get_jwt
from models.invalid_tokens import InvalidToken


class User(BaseModel, db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)
    password_reset_confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        """initializes user"""
        super().__init__(**kwargs)
        if kwargs and kwargs.get('password', None):
            password_hash = md5(kwargs['password'].encode('utf-8'))
            self.password = password_hash.hexdigest()

    @classmethod
    def get_current_user(cls):
        id = get_jwt_identity()
        return cls.query.filter_by(id=id).first()

    def set_password(self, password):
        password_hash = md5(password.encode('utf-8'))
        self.password = password_hash.hexdigest()

    def generate_confirmation_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], 'confirmation')
        return s.dumps({'confirm': self.email})

    def generate_password_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], 'password')
        return s.dumps({'password': self.id})

    def send_account_confirmation_link(self, token):
        msg = Message(subject='Confirm Your Account',
                      sender=current_app.config['MAIL_SENDER'],
                      recipients=[self.email]
        )
        msg.body = render_template('auth/confirmation_email.txt', user=self,
                                   token=token)
        mail.send(msg)

    def send_password_reset_link(self, token):
        msg = Message(subject='Reset Your Password',
                      sender=current_app.config['MAIL_SENDER'],
                      recipients=[self.email]
        )
        msg.body = render_template('auth/password_reset_email.txt', user=self,
                                   token=token)
        mail.send(msg)

    def authenticate_user(self, password):
        password_hash = md5(password.encode('utf-8'))
        return self.password == password_hash.hexdigest()

    def schedule_deletion(self):
        """Schedule a one-time job to delete the user if not confirmed after delay."""
        def delete_unverified_user():
            if not self.confirmed:
                db.remove(self)

        run_time = datetime.now(datetime.UTC) + timedelta(minutes=10)
        scheduler.add_job(func=delete_unverified_user, trigger='date', run_time=run_time)
