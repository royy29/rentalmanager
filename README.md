# Rental Manager API

This is a RESTful API built with FastAPI for managing vehicle rentals. It allows you to manage vehicles, users, and rental records. It also includes a background task for bulk vehicle import using Celery.

## Overview

This project provides the following functionalities:

- **Vehicle Management:** Add, list, retrieve, and bulk import vehicles.
- **User Management:** Create, list, and retrieve users.
- **Rental Management:** Create, list, retrieve, mark rentals as returned, and delete rentals.
- **Combined User Onboarding and Rental:** Create a new user and immediately rent a vehicle to them.
- **Asynchronous Bulk Import:** Upload a CSV file to add multiple vehicles in the background using Celery.

## Project Structure

Markdown

# Rental Manager API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

This is a RESTful API built with FastAPI for managing vehicle rentals. It allows you to manage vehicles, users, and rental records. It also includes a background task for bulk vehicle import using Celery.

## Overview

This project provides the following functionalities:

- **Vehicle Management:** Add, list, retrieve, and bulk import vehicles.
- **User Management:** Create, list, and retrieve users.
- **Rental Management:** Create, list, retrieve, mark rentals as returned, and delete rentals.
- **Combined User Onboarding and Rental:** Create a new user and immediately rent a vehicle to them.
- **Asynchronous Bulk Import:** Upload a CSV file to add multiple vehicles in the background using Celery.

## Project Structure

Rental Manager/
├── README.md
├── .gitignore
└── app/
├── init.py
├── crud.py
├── database.py
├── main.py
├── models.py
├── schemas.py
├── celery_app/
│   ├── init.py
│   └── tasks.py
└── routers/
├── rentals.py
├── users.py
└── vehicles.py


- `main.py`: FastAPI application initialization and includes all the API routers.
- `database.py`: Sets up the SQLAlchemy engine, session factory, and base for ORM models.
- `models.py`: Defines the SQLAlchemy ORM models for `Vehicle`, `User`, and `Rental`.
- `schemas.py`: Contains Pydantic schemas used for request and response data validation.
- `crud.py`: Implements the Create, Read, Update, and Delete (CRUD) operations for the database models.
- `routers/`: A directory containing separate route handlers for `vehicles`, `users`, and `rentals`.
- `celery_app/`: Contains the Celery application instance and background tasks, such as the bulk vehicle import.

## API Endpoints

### Vehicles (`/vehicles`)

- **`POST /vehicles/`**: Create a new vehicle.
    - **Request Body**: `VehicleCreate` schema.
    - **Response**: `Vehicle` object.
- **`GET /vehicles/`**: List all vehicles (with optional pagination).
    - **Query Parameters**:
        - `skip` (integer, optional): Number of items to skip for pagination. Default is `0`.
        - `limit` (integer, optional): Maximum number of items to return. Default is `100`.
    - **Response**: List of `Vehicle` objects.
- **`GET /vehicles/{vehicle_id}`**: Get details of a specific vehicle by ID.
    - **Path Parameter**: `vehicle_id` (integer).
    - **Response**: `Vehicle` object.
- **`POST /vehicles/upload/`**: Upload a CSV file for bulk vehicle creation (background task via Celery).
    - **Request**: Multipart file upload (`.csv`).
    - **Response**: JSON object with a message indicating background processing.

### Users (`/users`)

- **`POST /users/`**: Create a new user.
    - **Request Body**: `UserCreate` schema.
    - **Response**: `User` object.
- **`GET /users/`**: List all users.
    - **Response**: List of `User` objects.
- **`GET /users/{user_id}`**: Get details of a specific user by ID.
    - **Path Parameter**: `user_id` (integer).
    - **Response**: `User` object.
- **`POST /users/onboard_rent/`**: Onboard a new user and immediately create a rental for a specified vehicle.
    - **Request Body**: `OnboardUserRental` schema (includes user information, `vehicle_id`, and `expected_return`).
    - **Response**: JSON object containing the created `User` and `Rental` objects.

### Rentals (`/rentals`)

- **`POST /rentals/`**: Create a new rental.
    - **Request Body**: `RentalCreate` schema.
    - **Response**: `Rental` object.
- **`GET /rentals/`**: List all rentals.
    - **Response**: List of `Rental` objects.
- **`GET /rentals/{rental_id}`**: Get details of a specific rental by ID.
    - **Path Parameter**: `rental_id` (integer).
    - **Response**: `Rental` object.
- **`POST /rentals/{rental_id}/return`**: Mark a rental as returned (sets `actual_return` timestamp and makes the associated vehicle available).
    - **Path Parameter**: `rental_id` (integer).
    - **Response**: Updated `Rental` object.
- **`DELETE /rentals/{rental_id}`**: Delete a rental by ID.
    - **Path Parameter**: `rental_id` (integer).
    - **Response**: HTTP 204 No Content.

## Additional Notes

- **Celery Integration**: The API leverages Celery and Redis for asynchronous task processing, specifically for handling bulk vehicle imports from CSV files.
- **Database**: The project is configured to use SQLite for development, which can be easily switched to PostgreSQL or other databases for production environments by modifying the `database.py` file.
- **ORM Models**: SQLAlchemy is used as the Object-Relational Mapper (ORM) to interact with the database. The relationships between `Vehicle`, `User`, and `Rental` models are defined using foreign keys.
- **Data Validation**: Pydantic schemas are used extensively for request and response body validation, ensuring data integrity and providing clear error messages.

## Getting Started (Example - Development Environment)

1.  **Clone the repository** (if you have one):
    ```bash
    git clone <repository_url>
    cd Rental Manager
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate  # On Windows
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt  # You'll need to create this file
    pip install uvicorn sqlalchemy alembic psycopg2-binary # Example for PostgreSQL
    pip install fastapi python-multipart # For FastAPI and file uploads
    pip install celery redis
    ```
    *(Note: You'll need to create a `requirements.txt` file listing all dependencies.)*

4.  **Set up the database:**
    - For SQLite, the database file (`./app.db`) will be created automatically.
    - For other databases like PostgreSQL, configure the database URL in `database.py` and run Alembic migrations to create the tables:
      ```bash
      cd app
      alembic upgrade head
      ```

5.  **Start the Redis server (for Celery):**
    ```bash
    redis-server
    ```

6.  **Start the Celery worker:**
    ```bash
    celery -A app.celery_app worker -l info
    ```
    *(Make sure your `celery_app` instance is correctly configured in `app/celery_app/tasks.py` and imported in `main.py`)*

7.  **Run the FastAPI application:**
    ```bash
    uvicorn app.main:app --reload
    ```

8.  **Access the API:** The API will be accessible at `http://127.0.0.1:8000`. You can use tools like Swagger UI (usually available at `http://127.0.0.1:8000/docs`) or Postman to interact with the endpoints.

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature`).
3.  Make your changes.
4.  Commit your changes (`git commit -am 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature`).
6.  Create a new Pull Request.
