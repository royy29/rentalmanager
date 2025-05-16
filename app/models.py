from sqlalchemy import Column, Integer, String, Boolean
from .database import Base
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    registration_number = Column(String, unique=True, index=True)
    is_available = Column(Boolean, default=True)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    contact = Column(String, nullable=False)

    rentals = relationship("Rental", back_populates="user")


class Rental(Base):
    __tablename__ = "rentals"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    rent_start = Column(DateTime, default=datetime.utcnow)
    expected_return = Column(DateTime)
    actual_return = Column(DateTime, nullable=True)

    vehicle = relationship("Vehicle")
    user = relationship("User", back_populates="rentals")
