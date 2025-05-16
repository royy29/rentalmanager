from fastapi import FastAPI
from app.routers import vehicles, users, rentals
from app.database import Base, engine
from app import models

app = FastAPI(title="Rental Vehicle Manager")

app.include_router(vehicles.router)
app.include_router(rentals.router)
app.include_router(users.router)


Base.metadata.create_all(bind=engine)