#!/usr/bin/python3
"""module for testing db storage"""
import unittest
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from models import storage
import os
from models.engine import db_Storage
from random import choice


class test_db_Storage(unittest.TestCase):
    """class to test the db storage methods"""

    def test_module_doc(self):
        self.assertTrue(len(db_Storage.__doc__) > 1)

    def test_class_doc(self):
        self.assertTrue(len(db_Storage.DBStorage
                                      .__doc__) > 1)

    def test_init_doc(self):
        self.assertTrue(len(db_Storage.DBStorage
                                      .__init__
                                      .__doc__) > 1)

    def test_all(self):
        cls_list = [None, User, State, Review,
               Place, City, BaseModel]
        classe = choice(cls_dict)
        DBStorage = db_Storage.DBStorage
        assertTrue(type(DBStorage.all(classe)) is dict)
