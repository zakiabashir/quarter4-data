import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import get_db, Base
from models.user import User
from middleware.auth import get_password_hash, create_access_token

# Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def test_user():
    """Create a test user"""
    user = User(
        email="test@example.com",
        name="Test User",
        password=get_password_hash("testpassword123"),
        role="student"
    )
    return user

class TestAuthentication:
    """Test authentication endpoints"""

    def test_register_user(self, client, setup_database):
        """Test user registration"""
        user_data = {
            "email": "newuser@example.com",
            "name": "New User",
            "password": "TestPass123",
            "role": "student"
        }

        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 200

        data = response.json()
        assert data["email"] == "newuser@example.com"
        assert data["name"] == "New User"
        assert "id" in data

    def test_register_duplicate_email(self, client, setup_database, test_user):
        """Test registration with duplicate email"""
        db = TestingSessionLocal()
        db.add(test_user)
        db.commit()

        user_data = {
            "email": "test@example.com",
            "name": "Another User",
            "password": "TestPass123"
        }

        response = client.post("/api/v1/auth/register", json=user_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_login_success(self, client, setup_database, test_user):
        """Test successful login"""
        db = TestingSessionLocal()
        db.add(test_user)
        db.commit()

        login_data = {
            "username": "test@example.com",
            "password": "testpassword123"
        }

        response = client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 200

        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert "user" in data

    def test_login_invalid_credentials(self, client):
        """Test login with invalid credentials"""
        login_data = {
            "username": "nonexistent@example.com",
            "password": "wrongpassword"
        }

        response = client.post("/api/v1/auth/login", data=login_data)
        assert response.status_code == 401

    def test_get_current_user(self, client, setup_database, test_user):
        """Test getting current authenticated user"""
        db = TestingSessionLocal()
        db.add(test_user)
        db.commit()

        # Login to get token
        login_data = {
            "username": "test@example.com",
            "password": "testpassword123"
        }
        login_response = client.post("/api/v1/auth/login", data=login_data)
        token = login_response.json()["access_token"]

        # Get current user
        headers = {"Authorization": f"Bearer {token}"}
        response = client.get("/api/v1/auth/me", headers=headers)

        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["name"] == "Test User"

    def test_protected_endpoint_without_token(self, client):
        """Test accessing protected endpoint without token"""
        response = client.get("/api/v1/auth/me")
        assert response.status_code == 401

    def test_token_verification(self, client, setup_database, test_user):
        """Test token verification endpoint"""
        db = TestingSessionLocal()
        db.add(test_user)
        db.commit()

        # Create valid token
        token = create_access_token(data={"sub": test_user.id})

        response = client.get(f"/api/v1/auth/verify-token?token={token}")
        assert response.status_code == 200

        data = response.json()
        assert data["valid"] is True
        assert data["user_id"] == test_user.id

if __name__ == "__main__":
    pytest.main([__file__, "-v"])