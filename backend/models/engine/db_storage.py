#!/usr/bin/python3
"""
Modules models the db ORM
"""
from flask_sqlalchemy import SQLAlchemy


class DBStorage(SQLAlchemy):
    """Defines the db ORM class"""
    def save(self, obj):
        """saves an object to the database

        Args:
            obj: an object to save
        """
        self.session.add(obj)
        self.session.commit()

    def remove(self, obj):
        """deletes an object from the database

        Args:
            obj: an object to delete
        """
        self.session.delete(obj)
        self.session.commit()

    def fetch_all(self, name, type):
        """Fetches all resource instance of a given name and type

        Args:
            name -> str: the name of the resource
            type -> str: the resource type
        """
        from models.resource import Resource
        return Resource.query.filter_by(name=name, type=type).all()
