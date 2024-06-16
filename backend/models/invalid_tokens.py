#!/user/bin/python3
"""
Module defines a model for invalid session tokens
"""
from models.base_model import BaseModel
from models import db


class InvalidToken(BaseModel, db.Model):
    __tablename__ = 'invalid_tokens'
    jti = db.Column(db.String(36), nullable=False, index=True)

    @classmethod
    def is_valid(cls, jti):
        """checks if the token is blacklisted"""
        return bool(cls.query.filter_by(jti=jti).first())
