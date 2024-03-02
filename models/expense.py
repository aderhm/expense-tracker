#!/usr/bin/python3
"""Contains class Expense.
"""

import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship


class Expense(BaseModel, Base):
    """Represents an expense.
    """
    __tablename__ = "expenses"
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    category = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    amount = Column(Integer, nullable=False, default=0)

    def __init__(self, *args, **kwargs):
        """Initializes Expense.
        """
        super().__init__(*args, **kwargs)
