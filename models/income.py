#!/usr/bin/python3
"""Contains class Income.
"""

import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Income(BaseModel, Base):
    """Represents an expense.
    """
    __tablename__ = "incomes"
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    category = Column(String(128), nullable=False)
    amount = Column(Integer, nullable=False, default=0)

    def __init__(self, *args, **kwargs):
        """Initializes Income.
        """
        super().__init__(*args, **kwargs)
