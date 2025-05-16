from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class VehicleBase(BaseModel):
    name: str
    type: str
    registration_number: str

class VehicleCreate(VehicleBase):
    pass

class Vehicle(VehicleBase):
    id: int
    is_available: bool

    class Config:
        orm_mode = True


# User schemas
class UserBase(BaseModel):
    name: str
    contact: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    class Config:
        orm_mode = True


# Rental schemas
class RentalBase(BaseModel):
    vehicle_id: int
    user_id: int
    expected_return: datetime

class RentalCreate(RentalBase):
    pass

class Rental(RentalBase):
    id: int
    rent_start: datetime
    actual_return: Optional[datetime]

    class Config:
        orm_mode = True
