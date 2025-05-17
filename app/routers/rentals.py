from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas
from ..database import SessionLocal

router = APIRouter(prefix="/rentals", tags=["rentals"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Rental)
def create_rental(rental: schemas.RentalCreate, db: Session = Depends(get_db)):
    return crud.create_rental(db, rental)

@router.get("/", response_model=list[schemas.Rental])
def read_rentals(db: Session = Depends(get_db)):
    return crud.get_rentals(db)

@router.get("/{rental_id}", response_model=schemas.Rental)
def read_rental(rental_id: int, db: Session = Depends(get_db)):
    db_rental = crud.get_rental(db, rental_id)
    if db_rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    return db_rental

@router.post("/{rental_id}/return", response_model=schemas.Rental)
def return_vehicle(rental_id: int, db: Session = Depends(get_db)):
    rental = crud.return_vehicle(db, rental_id)
    if rental is None:
        raise HTTPException(status_code=404, detail="Rental not found")
    return rental

@router.delete("/{rental_id}", status_code=204)
def delete_rental(rental_id: int, db: Session = Depends(get_db)):
    success = crud.delete_rental(db, rental_id)
    if not success:
        raise HTTPException(status_code=404, detail="Rental not found")
    return

