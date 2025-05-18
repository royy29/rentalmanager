# rentalmanager
A vehicle rental manager platform.

Key Modules
main.py: FastAPI app initialization and router inclusion.
database.py: SQLAlchemy engine, session, and base setup.
models.py: SQLAlchemy ORM models for Vehicle, User, Rental.
schemas.py: Pydantic schemas for request/response validation.
crud.py: CRUD operations for vehicles, users, rentals.
routers/: API route definitions for vehicles, users, rentals.
celery_app/: Celery configuration and background task for bulk vehicle import.
API Endpoints
Vehicles (/vehicles)
POST /vehicles/

Create a new vehicle.
Request body: VehicleCreate schema.
Response: Created Vehicle.
GET /vehicles/

List all vehicles (with optional pagination).
Query params: skip, limit.
Response: List of Vehicle.
GET /vehicles/{vehicle_id}

Get details of a specific vehicle by ID.
Response: Vehicle.
POST /vehicles/vehicles/

Upload a CSV file for bulk vehicle creation (background task via Celery).
Request: Multipart file upload (.csv).
Response: Message indicating background processing.
Users (users)
POST users

Create a new user.
Request body: UserCreate schema.
Response: Created User.
GET users

List all users.
Response: List of User.
GET /users/{user_id}

Get details of a specific user by ID.
Response: User.
POST /users/Onboard&Rent

Onboard a new user and immediately create a rental for a specified vehicle.
Request body: OnboardUserRental schema (includes user info, vehicle ID, expected return).
Response: Created User and Rental objects.
Rentals (/rentals)
POST /rentals/

Create a new rental.
Request body: RentalCreate schema.
Response: Created Rental.
GET /rentals/

List all rentals.
Response: List of Rental.
GET /rentals/{rental_id}

Get details of a specific rental by ID.
Response: Rental.
POST /rentals/{rental_id}/return

Mark a rental as returned (sets actual_return and makes vehicle available).
Response: Updated Rental.
DELETE /rentals/{rental_id}

Delete a rental by ID.
Response: No content (204).

Additional Notes
Celery Integration: Bulk vehicle import via CSV is handled asynchronously using Celery and Redis.
Database: SQLite is used for development; can be swapped for PostgreSQL in production.
Models: Vehicles, Users, and Rentals are related via foreign keys and SQLAlchemy relationships.
Validation: All request/response bodies are validated using Pydantic schemas.
