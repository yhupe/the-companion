import pytest
from application.app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_home_route(client):
    response = client.get("/")
    assert response.status_code == 418
    assert response.json == {"message": "I am a Teapot"}

def test_status_route(client):
    response = client.get("/status")
    assert response.status_code == 200
    assert response.json == {"message": "Up and running"}
