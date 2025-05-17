from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/users", tags=["users"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)

@router.get("/", response_model=list[schemas.User])
def read_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@router.get("/{user_id}", response_model=schemas.User)
def read_users(user_id:int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user in None:
        raise HTTPException(status_code=404, detail="user Not Found")
    return db_user

@router.post("/Onboard&Rent")
def onboard_user_and_rent(data: schemas.OnboardUserRental, db: Session = Depends(get_db)):
    #Create user
    new_user = crud.create_user(db, schemas.UserCreate(name=data.name, contact=data.contact))
    
    #Check vehicle avail
    vehicle = crud.get_vehicle(db, data.vehicle_id)
    if not vehicle or not vehicle.is_available:
        raise HTTPException(status_code=400, detail="Vehicle not available")

    #Create rental using new user id
    rental_data = schemas.RentalCreate(
        vehicle_id=data.vehicle_id,
        user_id=new_user.id,
        expected_return=data.expected_return
    )
    new_rental = crud.create_rental(db, rental_data)

    return {
        "user": new_user,
        "rental": new_rental
    }