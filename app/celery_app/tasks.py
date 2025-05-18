import csv
from io import StringIO
from app import models
from app.database import SessionLocal
from app.celery_app import celery_app
from .. import crud
import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session



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

@celery_app.task
def process_bulk_users(file_data: str):
    db = SessionLocal()
    reader = csv.DictReader(StringIO(file_data))
    for row in reader:
        user = models.User(
            name=row['name'],
            email=row['email']
        )
        db.add(user)
    db.commit()
    db.close()


@celery_app.task
def send_rental_conf_email(rental_id: int):
    db = SessionLocal()
    try:
        rental = crud.get_rental(db, rental_id)
        if not rental:
            logging.error(f"Rental with ID {rental_id} not found.")
            return
        
        user = crud.get_user(db, rental.user_id)
        vehicle = crud.get_vehicle(db, rental.vehicle_id)
        if not user or not vehicle:
            logging.error(f"User or Vehicle data missing for Rental ID {rental_id}.")
            return

        # Construct the email content
        to_email = user.contact
        subject = "Rental Confirmation"
        body = (
            f"Dear {user.name},\n\n"
            f"Thank you for renting with us! Here are your rental details:\n"
            f"Vehicle: {vehicle.name} {vehicle.registration_number}\n"
            f"Rental Start: {rental.rent_start}\n"
            f"Rental End: {rental.expected_return}\n\n"
            f"Enjoy your ride!\n"
        )

        # Simulate sending the email
        send_email(to_email, subject, body)
        logging.info(f"Rental confirmation email sent to {to_email} for Rental ID {rental_id}.")
    except Exception as e:
        logging.error(f"Error sending rental confirmation email for Rental ID {rental_id}: {e}")
    finally:
        db.close()

# Placeholder function for sending emails
def send_email(to_email: str, subject: str, body: str):
    # Simulate email sending (implementation not required)
    print(f"Email sent to {to_email} with subject '{subject}' and body:\n{body}")


@celery_app.task(name="app.celery_app.tasks.send_return_reminders")
def send_return_reminders():
    db: Session = SessionLocal()
    try:
        tomorrow = datetime.now() + timedelta(days=1)
        upcoming_rentals = db.query(models.Rental).filter(
            models.Rental.expected_return >= datetime.now(),
            models.Rental.expected_return < tomorrow,
            models.Rental.actual_return == None, 
        ).all()

        for rental in upcoming_rentals:
            user = crud.get_user(db, rental.user_id)
            vehicle = crud.get_vehicle(db, rental.vehicle_id)

            if not user or not vehicle:
                continue

            subject = "Rental Return Reminder"
            body = (
                f"Dear {user.name},\n\n"
                f"This is a friendly reminder to return your rental vehicle tomorrow.\n\n"
                f"Vehicle: {vehicle.name} ({vehicle.registration_number})\n"
                f"Expected Return: {rental.expected_return.strftime('%Y-%m-%d %H:%M')}\n\n"
                f"Thank you!"
            )

            send_email(user.contact, subject, body)
            logging.info(f"Sent return reminder to {user.contact}")
    except Exception as e:
        logging.error(f"Error in sending return reminders: {e}")
    finally:
        db.close()