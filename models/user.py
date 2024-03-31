#!/usr/bin/python3
"""
User
"""
from models.base_model import BaseModel, Base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String


class User(BaseModel, Base):
    """
    User class representing a user entity.
    """
    __tablename__ = 'users'

    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)
    first_name = Column(String(128), nullable=True)
    last_name = Column(String(128), nullable=True)

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of User.
        """
        super().__init__(*args, **kwargs)
