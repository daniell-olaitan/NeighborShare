#!/usr/bin/python3
"""
Module defines the Conversation model
"""
from models.base_model import BaseModel
from models import db


class Conversation(BaseModel, db.Model):
    __tablename__ = 'conversations'
    resource_id = db.Column(db.String(60), db.ForeignKey('resources.id'),
                        nullable=False)
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'),
                        nullable=False)
    name = db.Column(db.String(60), nullable=False)
    resource = db.relationship('Resource', backref='requests',
                           cascade='delete', lazy='dynamic')
    user = db.relationship('User', backref='requests',
                           cascade='delete', lazy='dynamic')
