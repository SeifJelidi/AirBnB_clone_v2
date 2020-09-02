#!/usr/bin/python3
"""New engine DBStorage"""
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from os import environ, getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """DBStorage Class"""
    __engine = None
    __session = None

    def __init__(self):
        """constructor of DBStorage"""

        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        hbn_env = getenv('HBNB_ENV')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, password, host, database), pool_pre_ping=True)

        if hbn_env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        '''displays all objects'''
        objects = {}
        classes = ["User", "State", "City", "Amenity", "Place", "Review"]
        if cls is None:
            for c in classes:
                objs = self.__session.query(eval(c))
            for obj in objs:
                k = "{}.{}".format(type(obj).__name__, obj.id).all()
                objects[k] = obj
        else:
            objs = self.__session.query(cls).all()
            for obj in objects:
                k = "{}.{}".format(type(obj).__name__, obj.id)
                objects[k] = obj
        return objects

    def new(self, obj):
        '''adds a new object'''
        if obj:
            self.__session.add(obj)

    def save(self):
        '''commits all changes'''
        self.__session.commit()

    def delete(self, obj=None):
        '''deletes an object from db'''
        if obj is not None:
            self.__session.delete(eval(obj))

    def reload(self):
        '''creates all tables in the database'''
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        session = scoped_session(Session)
        self.__session = session()

    def close(self):
        '''closes session'''
        self.__session.close()
