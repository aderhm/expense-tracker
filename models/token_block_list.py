#!/usr/bin/python3
"""Contains class TokenBlockList.
"""

import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String


class TokenBlockList(BaseModel, Base):
    """Represents a token block list
    """
    __tablename__ = "tokens_block_list"
    jti = Column(String(128), nullable=False)

    def __init__(self, *args, **kwargs):
        """Initializes the User.
        """
        super().__init__(*args, **kwargs)
