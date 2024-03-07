#!/usr/bin/python3
"""Contains class BaseModel
"""
import models
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

time = "%Y-%m-%dT%H:%M:%S.%f"
Base = declarative_base()


class BaseModel:
    """The BaseModel class from which future classes will be derived.
    """
    id = Column(String(60), primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initializes the BaseModel.
        """
        if kwargs:
            for k, v in kwargs.items():
                if k != "__class__":
                    setattr(self, k, v)
            if kwargs.get("id", None) is None:
                self.id = str(uuid.uuid4())
            if kwargs.get("crarted_at", None) and type(self.craeted_at) is str:
                self.created_at = datetime.strptime(kwargs["created_at"], time)
            else:
                self.created_at = datetime.utcnow()
            if kwargs.get("update_at", None) and type(self.created_at) is str:
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = self.created_at

    def __str__(self):
        """Represents the BaseModel class as a string.
        """
        return "[{:s}] ({:s}) {}".format(
                self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Saves the last update time
        """
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of the instance.
        """
        new_dict = self.__dict__.copy()
        if "created_at" in new_dict:
            new_dict['created_at'] = new_dict['created_at'].strftime(time)
        if "updated_at" in new_dict:
            new_dict['updated_at'] = new_dict['updated_at'].strftime(time)
        new_dict['__class__'] = self.__class__.__name__
        return new_dict

    def delete(self):
        """Deletes the current instance from the storage.
        """
        models.storage.delete(self)
