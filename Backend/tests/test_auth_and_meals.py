import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database.session import get_db
from app.models.user_model import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Use SQLite in-memory test DB
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Override dependency
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_register_user():
    payload = {
        "first_name": "Test",
        "last_name": "User",
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 200
    assert response.json()["email"] == payload["email"]

def test_login_user():
    payload = {
        "email": "test@example.com",
        "password": "password123"
    }
    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    global token
    token = response.json()["access_token"]

def test_get_calories_invalid_serving():
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/get-calories", json={"dish_name": "pasta", "servings": 0}, headers=headers)
    assert response.status_code == 400
    assert "Invalid servings" in response.json()["detail"]

def test_get_calories_invalid_dish():
    headers = {"Authorization": f"Bearer {token}"}
    response = client.post("/api/get-calories", json={"dish_name": "zzzzzzzz", "servings": 1}, headers=headers)
    assert response.status_code == 404

def test_get_meal_history():
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/meals", headers=headers)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
