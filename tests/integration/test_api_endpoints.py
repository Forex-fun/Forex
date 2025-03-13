import pytest
from fastapi.testclient import TestClient
from src.api.app import app
from src.database import get_db, engine
from src.auth.models import Base, User
import jwt
import config
from datetime import datetime, timedelta

@pytest.fixture(scope="module")
def test_db():
    # Create test database
    Base.metadata.create_all(bind=engine)
    yield
    # Clean up
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def test_user(test_db):
    user = User(
        email="test@example.com",
        username="testuser",
        hashed_password=User.hash_password("testpass"),
        wallet_address="0x1234567890"
    )
    db = next(get_db())
    db.add(user)
    db.commit()
    return user

@pytest.fixture
def auth_token(test_user):
    token = jwt.encode(
        {
            "sub": test_user.username,
            "exp": datetime.utcnow() + timedelta(minutes=30)
        },
        config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM
    )
    return token

def test_health_check(test_client):
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_predict_endpoint_unauthorized(test_client):
    response = test_client.post("/predict", json={
        "symbol": "BTC-USD",
        "stake_amount": 0.1
    })
    assert response.status_code == 401

def test_predict_endpoint_authorized(test_client, auth_token):
    response = test_client.post(
        "/predict",
        json={
            "symbol": "BTC-USD",
            "stake_amount": 0.1
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "predicted_price" in data
    assert "confidence_score" in data

def test_chart_endpoint(test_client, auth_token):
    response = test_client.get(
        "/chart/BTC-USD?chart_type=price",
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "layout" in data 