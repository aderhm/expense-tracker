#!/usr/bin/python3
"""Initilize the models package
"""

from models.engine.db_storage import DBStorage

storage = DBStorage()
storage.reload()
