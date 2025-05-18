# Rental Manager API

This is a RESTful API built with FastAPI for managing vehicle rentals. It allows you to manage vehicles, users, and rental records. It also includes a background task for bulk vehicle import using Celery.

## Overview

This project offers the following key features:

- **Vehicle Management:** Add, list, retrieve, and efficiently import vehicles in bulk. Track vehicle availability status.
- **User Management:** Create, list, and retrieve user information. Streamlined user onboarding with immediate rental capabilities.
- **Rental Management:** Create, list, retrieve, process returns, and remove rental records. Automatically manages vehicle availability upon rental and return.
- **Asynchronous Task Processing:** Leverages Celery for background tasks such as bulk data imports and sending rental confirmation emails.
- **Scheduled Reminders:** Implements scheduled tasks using Celery Beat to send timely reminders for upcoming rental returns.

## Project Structure

- `main.py`: FastAPI application initialization and includes all API routers.
- `database.py`: Configures the SQLAlchemy engine, session factory, and base for ORM models.
- `models.py`: Defines the SQLAlchemy ORM models for `Vehicle`, `User`, and `Rental`, establishing database schema and relationships.
- `schemas.py`: Contains Pydantic schemas for request and response data validation, ensuring data integrity.
- `crud.py`: Implements the Create, Read, Update, and Delete (CRUD) operations for interacting with the database models.
- `routers/`: A directory housing separate route handlers for `vehicles`, `users`, and `rentals`, defining API endpoints.
- `celery_app/`: Contains the Celery application instance and defines asynchronous tasks, including bulk imports and email sending.
- `tests/`: Contains the pytest application instance and defines different usecases to test API Endpoints functioning.

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
- **`GET /vehicles/{vehicle_id}`**: Retrieve a specific vehicle by ID.
    - **Path Parameter**: `vehicle_id` (integer).
    - **Response**: `Vehicle` object.
- **`POST /vehicles/vehicles_bulk/`**: Bulk import vehicles from a CSV file.
    - **Request**: Multipart file upload (`.csv`).
    - **Response**: JSON message indicating background processing.

### Users (`/users`)

- **`POST /users/`**: Create a new user.
    - **Request Body**: `UserCreate` schema.
    - **Response**: `User` object.
- **`GET /users/`**: List all users.
    - **Response**: List of `User` objects.
- **`GET /users/{user_id}`**: Retrieve a specific user by ID.
    - **Path Parameter**: `user_id` (integer).
    - **Response**: `User` object.
- **`POST /users/onboard_rent/`**: Onboard a new user and immediately rent a vehicle.
    - **Request Body**: `OnboardUserRental` schema (includes user details, `vehicle_id`, and `expected_return`).
    - **Response**: JSON object containing the created `User` and `Rental`.
- **`POST /users/users_bulk/`**: Bulk import users from a CSV file.
    - **Request**: Multipart file upload (`.csv`).
    - **Response**: JSON message indicating background processing.

### Rentals (`/rentals`)

- **`POST /rentals/`**: Create a new rental.
    - **Request Body**: `RentalCreate` schema.
    - **Response**: `Rental` object.
- **`GET /rentals/`**: List all rentals.
    - **Response**: List of `Rental` objects.
- **`GET /rentals/{rental_id}`**: Retrieve a specific rental by ID.
    - **Path Parameter**: `rental_id` (integer).
    - **Response**: `Rental` object.
- **`POST /rentals/{rental_id}/return`**: Mark a rental as returned (sets `actual_return` timestamp and makes the associated vehicle available).
    - **Path Parameter**: `rental_id` (integer).
    - **Response**: Updated `Rental` object.
- **`DELETE /rentals/{rental_id}`**: Delete a rental by ID.
    - **Path Parameter**: `rental_id` (integer).
    - **Response**: HTTP 204 No Content.

## Additional Notes

- **Celery Integration**: The API leverages Celery and Redis for asynchronous task processing, including bulk imports and sending rental confirmation emails.
- **Scheduled Reminders**: Celery Beat is used to schedule periodic tasks, such as sending reminders for upcoming rental returns.
- **Database**: The project is configured to use SQLite for development, which can be easily switched to PostgreSQL or other databases for production environments by modifying the `database.py` file.
- **ORM Models**: SQLAlchemy ORM models (`Vehicle`, `User`, `Rental`) define the database schema and relationships.
- **Data Validation**: Pydantic schemas are used extensively for request and response body validation, ensuring data integrity.

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
    pip install -r requirements.txt
    ```

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
    #or
    .\redis-server.exe redis.windows.conf
    ```

6.  **Start the Celery worker:**
    ```bash
    celery -A app.celery_app worker --loglevel=info --pool=solo
    ```
    *(Make sure your `celery_app` instance is correctly configured in `app/celery_app/tasks.py` and imported in `main.py`)*

7.  **Start the Celery Beat scheduler (for scheduled tasks like return reminders):**
    ```bash
    celery -A app.celery_app beat --loglevel=info
    ```
    *(Ensure Celery Beat is configured in your `celery_app` module, usually in `tasks.py`.)*

8.  **Run the FastAPI application:**
    ```bash
    uvicorn app.main:app --reload
    ```

9.  **Access the API:** The API will be accessible at `http://127.0.0.1:8000`. You can use tools like Swagger UI (usually available at `http://127.0.0.1:8000/docs`) or Postman to interact with the endpoints.

## Test Scenarios (using pytest)

This section outlines the pytest-based test scenarios for the Rental Manager API.

### 1. Test Rental Creation

**Use Case:** Verify successful rental creation when the vehicle is available.

**Test Steps:**

1.  Create a test vehicle and user.
2.  Call the `POST /rentals/` endpoint with valid rental data.
3.  **Assertions:**
    - Response status code is `200 OK`.
    - The rental is created in the database.
    - The associated vehicle's availability is marked as `unavailable`.

### 2. Test Rental Creation with Unavailable Vehicle

**Use Case:** Ensure rental creation fails for unavailable vehicles.

**Test Steps:**

1.  Create a test vehicle and mark it as `unavailable`.
2.  Call the `POST /rentals/` endpoint with the unavailable vehicle's ID.
3.  **Assertions:**
    - Response status code is `400 Bad Request`.
    - The response includes an error message indicating vehicle unavailability.

### 3. Test Rental Retrieval

**Use Case:** Verify retrieval of a rental by its ID.

**Test Steps:**

1.  Create a test rental.
2.  Call the `GET /rentals/{rental_id}` endpoint with the created rental's ID.
3.  **Assertions:**
    - Response status code is `200 OK`.
    - The response body contains the correct details of the retrieved rental.

### 4. Test Rental Return

**Use Case:** Verify marking a rental as returned and updating vehicle availability.

**Test Steps:**

1.  Create a test rental.
2.  Call the `POST /rentals/{rental_id}/return` endpoint with the rental's ID.
3.  **Assertions:**
    - Response status code is `200 OK`.
    - The `actual_return` field of the rental is updated in the database.
    - The associated vehicle's availability is marked as `available`.

### 5. Test Rental Deletion

**Use Case:** Verify successful deletion of a rental.

**Test Steps:**

1.  Create a test rental.
2.  Call the `DELETE /rentals/{rental_id}` endpoint with the rental's ID.
3.  **Assertions:**
    - Response status code is `204 No Content`.
    - The rental record is removed from the database.

## Contributing

Contributions are welcome! Please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature`).
3.  Make your changes.
4.  Commit your changes (`git commit -am 'Add some feature'`).
5.  Push to the branch (`git push origin feature/your-feature`).
6.  Create a new Pull Request.