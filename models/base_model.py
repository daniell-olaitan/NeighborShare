#!/usr/bin/python3
"""
Module defines the base model class
"""
import uuid
from models import db


class BaseModel:
    """class subclasses all the models in the application"""
    id = db.Column(db.String(60), primary_key=True, nullable=False)

    def __init__(self, **kwargs):
        if not kwargs:
            self.id = str(uuid.uuid4())
        else:
            if self.id == None:
                self.id = str(uuid.uuid4())

            self.__dict__.update(kwargs)
