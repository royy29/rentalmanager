# import csv
# from io import StringIO
# from app import models
# from app.database import SessionLocal
# from app.celery_app import celery_app


# @celery_app.task
# def process_bulk_vehicles(file_data: str):
#     db = SessionLocal()
#     reader = csv.DictReader(StringIO(file_data))
#     for row in reader:
#         vehicle = models.Vehicle(
#             name=row['name'],
#             type=row['type'],
#             registration_number=row['registration_number'],
#             is_available=row.get('is_available', 'True') == 'True'
#         )
#         db.add(vehicle)
#     db.commit()
#     db.close()

# app/celery_app/tasks.py

import csv
from io import StringIO
from app import models
from app.database import SessionLocal
from app.celery_app import celery_app

@celery_app.task
def process_bulk_vehicles(file_data: str):
    db = SessionLocal()
    reader = csv.DictReader(StringIO(file_data))
    for row in reader:
        vehicle = models.Vehicle(
            name=row['name'],
            type=row['type'],
            registration_number=row['registration_number'],
            is_available=row.get('is_available', 'True') == 'True'
        )
        db.add(vehicle)
    db.commit()
    db.close()
