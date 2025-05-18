# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from app.models import Base
# from app.main import app
# from fastapi.testclient import TestClient

# TEST_DATABASE_URL = "sqlite:///./test_rental_manager.db"

# engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
# TestingSessionLocal = sessionmaker(bind=engine)

# # Override get_db
# def override_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# @pytest.fixture(scope="module")
# def client():
#     # Recreate test database each time
#     Base.metadata.drop_all(bind=engine)
#     Base.metadata.create_all(bind=engine)

#     from app.routers import rentals
#     app.dependency_overrides[rentals.get_db] = override_get_db

#     with TestClient(app) as c:
#         yield c


import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base
from app.dependencies import get_db

TEST_DATABASE_URL = "sqlite:///./test_rental_manager.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables before tests run
Base.metadata.create_all(bind=engine)

# Dependency override
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Apply the override
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="function")
def client():
    yield TestClient(app)
