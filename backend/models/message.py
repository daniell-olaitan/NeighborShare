#!/usr/bin/python3
"""
Module defines the Message model
"""
from models.base_model import BaseModel
from models import db


class Message(BaseModel, db.Model):
    __tablename__ = 'messages'
    conversation_id = db.Column(db.String(60), db.ForeignKey('conversations.id'),
                        nullable=False)
    words = db.Column(db.String(2048), nullable=False)
    time = db.Column(db.DateTime(), nullable=False)
    conversation = db.relationship('Conversation', backref='messages',
                           cascade='delete', lazy='dynamic')
