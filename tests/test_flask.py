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
    assert response.json ==  {'API': '🟢', 'Conn_Twilio': '🟢', 'Database': '🟢', 'FOTH_MagicSauce': '🟢'}

def test_invalid_method(client):
    response = client.get("/whatsapp_incoming")
    assert response.status_code == 405


def test_post_request_form_data(client):
    response = client.post('/whatsapp_incoming',
                           data={"Body": "help",
                                 "From": "whatsapp:+14155238886"})
    exp_status_code = 200
    exp_response_data = b'<?xml version="1.0" encoding="UTF-8"?><Response><Message>Available commands: help, weather, journal, activities, advice, trivia</Message></Response>'
    assert response.status_code == exp_status_code
    assert response.data == exp_response_data

def test_post_request_form_data_command_unknown(client):
    response = client.post('/whatsapp_incoming',
                           data={"Body": "unknown command",
                                 "From": "whatsapp:+14155238886"})
    exp_status_code = 200
    exp_response_data = b'<?xml version="1.0" encoding="UTF-8"?><Response><Message>Unknown command. Send \'help\' for options.</Message></Response>'
    assert response.status_code == exp_status_code
    assert response.data == exp_response_data


def test_post_request_form_data_callback(client):
    response = client.post('/whatsapp_status_callback',
                           data={"MessageStatus": "read",
                                 "MessageSid": "SM1bf9b04c5c980db53f86a335ad6a67f"})
    exp_status_code = 200
    assert response.status_code == exp_status_code

