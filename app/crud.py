from sqlalchemy.orm import Session
from . import models, schemas
from datetime import datetime


def get_vehicles(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Vehicle).offset(skip).limit(limit).all()

def get_vehicle(db: Session, vehicle_id: int):
    return db.query(models.Vehicle).filter(models.Vehicle.id == vehicle_id).first()

def create_veh(db: Session, vehicle: schemas.VehicleCreate):
    db_vehicle = models.Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

# Users
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

# Rentals
def create_rental(db: Session, rental: schemas.RentalCreate):
    db_rental = models.Rental(**rental.dict())
    db.query(models.Vehicle).filter(models.Vehicle.id == rental.vehicle_id).update({"is_available": False})
    db.add(db_rental)
    db.commit()
    db.refresh(db_rental)
    return db_rental

def get_rentals(db: Session):
    return db.query(models.Rental).all()

def get_rental(db: Session, rental_id: int):
    return db.query(models.Rental).filter(models.Rental.id == rental_id).first()

def return_vehicle(db: Session, rental_id: int):
    rental = get_rental(db, rental_id)
    if rental:
        rental.actual_return = datetime.utcnow()
        db.query(models.Vehicle).filter(models.Vehicle.id == rental.vehicle_id).update({"is_available": True})
        db.commit()
        db.refresh(rental)
    return rental

def delete_rental(db: Session, rental_id: int):
    rental = db.query(models.Rental).filter(models.Rental.id == rental_id).first()
    if rental:
        db.delete(rental)
        db.commit()
        return True
    return False
