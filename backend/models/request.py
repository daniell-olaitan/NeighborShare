#!/usr/bin/python3
"""
Module defines the Request model
"""
from models.base_model import BaseModel
from models import db


class Request(BaseModel, db.Model):
    __tablename__ = 'requests'
    resource_id = db.Column(db.String(60), db.ForeignKey('resources.id'),
                        nullable=False)
    message = db.Column(db.String(2048))
    name = db.Column(db.String(60), nullable=False)
    resource = db.relationship('Resource', backref='requests',
                           cascade='delete', lazy='dynamic')
