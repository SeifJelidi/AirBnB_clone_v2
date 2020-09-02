#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import models
from models.city import City
from sqlalchemy import Column, String
from os import getenv
from sqlalchemy.orm import relationship, backref


class State(BaseModel, Base):
    """ State class """

    __tablename__ = "states"

    name = Column(String(128), nullable=False)
    if getenv('HBNB_TYPE_STORAGE') == "db":
        cities = relationship('City', cascade='all, delete-orphan',
                              backref='state')
    else:
        @property
        def cities(self):
            cts = []
            for id, c in models.storage.all(City).items():
                if self.id == c.state_id:
                    cts.append(c)
            return cts
