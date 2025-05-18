from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from .. import crud, schemas, models
from ..database import SessionLocal
from app.celery_app.tasks import process_bulk_vehicles

router = APIRouter(prefix="/vehicles", tags=["vehicles"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.Vehicle)
def create_vehicle(vehicle: schemas.VehicleCreate, db: Session = Depends(get_db)):
    return crud.create_veh(db, vehicle)

@router.get("/", response_model=list[schemas.Vehicle])
def read_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_vehicles(db, skip, limit)

@router.get("/{vehicle_id}", response_model=schemas.Vehicle)
def read_vehicle(vehicle_id: int, db: Session = Depends(get_db)):
    db_vehicle = crud.get_vehicle(db, vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

@router.post("/vehicles/")
async def upload_vehicle_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a CSV")

    content = await file.read()
    content_str = content.decode("utf-8")
    
    # Trigger Celery task
    process_bulk_vehicles.delay(content_str)
    return {"message": "File received. Processing in background."}
