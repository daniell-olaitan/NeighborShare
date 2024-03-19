#!/usr/bin/python3
"""
Module defines the Resource model
"""
from models import db
from models.base_model import BaseModel


class Resource(BaseModel, db.Model):
    __tablename__ = 'resources'
    user_id = db.Column(db.String(60), db.ForeignKey('users.id'),
                        nullable=False)
    latitude = db.Column(db.Float(), nullable=False)
    longitude = db.Column(db.Float(), nullable=False)
    status = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(2048))
    name = db.Column(db.String(60), nullable=False)
    type = db.Column(db.String(60), nullable=False)
    user = db.relationship('User', backref='resources',
                           cascade='delete', lazy='dynamic')
