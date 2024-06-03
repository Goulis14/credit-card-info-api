import pytest
from src.app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_verify_card_success(client, requests_mock):
    card_number = "45717360"
    mock_response = {
        "scheme": "visa",
        "type": "debit",
        "bank": {"name": "UBS"}
    }
    requests_mock.get(f"https://lookup.binlist.net/{card_number}", json=mock_response)

    response = client.get(f'/api/card-scheme/verify/{card_number}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert data['payload']['scheme'] == "visa"
    assert data['payload']['type'] == "debit"
    assert data['payload']['bank'] == "UBS"


def test_verify_card_not_found(client, requests_mock):
    card_number = "12345678"
    requests_mock.get(f"https://lookup.binlist.net/{card_number}", status_code=404)

    response = client.get(f'/api/card-scheme/verify/{card_number}')
    assert response.status_code == 404
    data = response.get_json()
    assert data['success'] is False
    assert data['message'] == "Card not found"