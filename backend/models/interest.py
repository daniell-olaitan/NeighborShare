#!/usr/bin/python3
"""
Module defines the Interest model
"""
from models.base_model import BaseModel
from models.resource import Resource
from models import db


class Interest(Resource, db.Model):
    def __init__(self):
        super().__init__()
        self.__tablename__ = 'interests'
        self.status = ''
