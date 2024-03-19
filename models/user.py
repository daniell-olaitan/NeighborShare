#!/usr/bin/python3
"""
Module defines the User model
"""
from flask_login import UserMixin, login_user, logout_user
from models.base_model import BaseModel
from models import db
from itsdangerous import TimedSerializer as Serializer
from flask import current_app, render_template, flash
from flask_mail import Message
from hashlib import md5
from app import login_manager, mail


class User(UserMixin, BaseModel, db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    home_address = db.Column(db.String(256), nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        """initializes user"""
        super().__init__(**kwargs)
        if kwargs and kwargs.get('password', None):
            password_hash = md5(kwargs['password'].encode('utf-8'))
            self.password = password_hash.hexdigest()

    def generate_confirmation_token(self):
        s = Serializer(current_app.config['SECRET_KEY'], 'confirmation')
        return s.dumps({'confirm': self.id})

    def confirm_token(self, token, max_age=600):
        s = Serializer(current_app.config['SECRET_KEY'], 'confirmation')
        try:
            data = s.loads(token, max_age=max_age)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        return True

    def confirm_account(self):
        token = self.generate_confirmation_token()
        msg = Message(subject='Confirm Your Account',
                      sender=current_app.config['MAIL_SENDER'],
                      recipients=[self.email]
        )
        msg.body = render_template('auth/confirmation_email.txt', user=self,
                                   token=token)

        mail.send(msg)
        flash('A confirmation email has been sent to you')

    def authenticate_user(self, password):
        password_hash = md5(password.encode('utf-8'))
        return self.password == password_hash.hexdigest()
        # return check_password_hash(self.password_hash, password)

    def signin_user(self, remember):
        login_user(self, remember)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)
