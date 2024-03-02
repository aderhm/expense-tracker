#!/usr/bin/python3
"""Contains class Goal.
"""

import datetime
import sqlalchemy
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship


class Goal(BaseModel, Base):
    """Represents an goal.
    """
    __tablename__ = "goals"
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    purpose = Column(String(128), nullable=False)
    target_amount = Column(Integer, nullable=False, default=0)
    monthly_saving_amount = Column(Integer, nullable=True)
    deadline = Column(Date, nullable=True)

    def __init__(self, *args, **kwargs):
        """Initializes Goal.
        """
        super().__init__(*args, **kwargs)
