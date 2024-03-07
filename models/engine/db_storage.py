#!/usr/bin/python3
"""Contains the class DBStorage
"""

import models
import sqlalchemy
from models.base_model import BaseModel, Base
from models.expense import Expense
from models.goal import Goal
from models.income import Income
from models.token_block_list import TokenBlockList
from models.user import User
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {
            "Expense": Expense,
            "Goal": Goal,
            "Income": Income,
            "User": User
        }


class DBStorage:
    """Interacts with the MySQL db.
    """
    __engine = None
    __session = None

    def __init__(self):
        """Initializes a DBStorage object.
        """
        ETA_DB_USER = getenv('ETA_DB_USER')
        ETA_DB_PWD = getenv('ETA_DB_PWD')
        ETA_DB_HOST = getenv('ETA_DB_HOST')
        ETA_DB_NAME = getenv('ETA_DB_NAME')
        self.__engine = create_engine("mysql+mysqldb://{}:{}@{}/{}".
                                      format(
                                          ETA_DB_USER,
                                          ETA_DB_PWD,
                                          ETA_DB_HOST,
                                          ETA_DB_NAME
                                          ))

    def all(self, cls=None):
        """Gets all from db.
        """
        _dict = {}
        for c in classes:
            if cls is None or cls is classes[c] or cls is c:
                objects = self.__session.query(classes[c]).all()
                for o in objects:
                    key = o.__class__.__name__ + '.' + o.id
                    _dict[key] = o
        return _dict

    def new(self, obj):
        """Adds a new object to the database.
        """
        self.__session.add(obj)

    def save(self):
        """Commits changes of the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the database.
        """
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Reloads data from the database.
        """
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(
                bind=self.__engine,
                expire_on_commit=False
                )
        sssn = scoped_session(session_factory)
        self.__session = sssn

    def close(self):
        """Remove the private session attribute.
        """
        self.__session.remove()

    def get(self, cls, id):
        """Retrieve object by id
        """
        if cls is not None and id is not None:
            return self.__session.query(cls).filter(cls.id == id).first()
        else:
            return None

    def check_account_existence(self, email):
        """Retrieve user by email.
        """
        if email is not None:
            return self.__session.query(User).filter(User.email == email).first()
        else:
            return None

    def get_token(self, jti):
        if jti is not None:
            return self.__session.query(TokenBlockList).filter(
                TokenBlockList.jti == jti
            ).scalar()
        else:
            return None

    def get_by_fk(self, cls, fk):
        """Retrieve objects by a foreign key.
        """
        if cls is not None and fk is not None:
            return self.__session.query(cls).filter(cls.user_id == fk).all()
        else:
            return None
