#!/usr/bin/python3
"""Contains class User.
"""

import models
import sqlalchemy
from hashlib import md5
from models import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Represents a user
    """
    __tablename__ = "users"
    username = Column(String(128), nullable=False)
    email = Column(String(128), nullable=False)
    password = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes The User.
        """
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """Sets a password with md5 encryption.
        """
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
