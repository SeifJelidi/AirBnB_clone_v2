#!/usr/bin/python3
""" Place Module for HBNB project """
import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy import ForeignKey, Table
from sqlalchemy.orm import relationship


plc_amty = Table('place_amenity', Base.metadata,
                 Column('place_id', String(60),
                        ForeignKey('places.id'),
                        nullable=False,
                        primary_key=True),
                 Column('amenity_id', String(60),
                        ForeignKey('amenities.id'),
                        nullable=False,
                        primary_key=True))


class Place(BaseModel, Base):
    """ Place Class """

    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    amenity_ids = []
    reviews = relationship("Review", backref="place", cascade="all, delete")
    amenities = relationship("Amenity", secondary="place_amenity")

    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def reviews(self):
            """ returns the review instances with
            place id  equals to Place.id """
            review = []
            rvs = models.storage.all(Review)
            for r in rvs.values():
                if r.id in self.id:
                    review.append(r)
            return review

        @property
        def amenities(self):
            """ get list of amenities """
            amenity = []
            amnts = models.storage.all(Amenity)
            for a in amnts.values():
                if a.id in self.amenity_ids:
                    amenity.append(a)
            return amenity

        @amenities.setter
        def amenities(self, obj):
            '''set ids of amenities'''
            if type(value) == Amenity:
                self.amenity_ids.append(value.id)
