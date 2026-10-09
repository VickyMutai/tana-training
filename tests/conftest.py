import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"

@pytest.fixture(scope="function")
def booking_data():
    return {
        "firstname": "QA",
        "lastname": "Tester",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2026-10-10",
            "checkout": "2026-10-12"
        },
        "additionalneeds": "Breakfast"
    }

@pytest.fixture(scope="session")
def auth_token():
    """Fixture to provide an authenticated token for testing."""
    response = requests.post(f"{BASE_URL}/auth", json={
        "username": "admin",
        "password": "password123"
    })
    assert response.status_code == 200, f"Authorization request failed: {response.text}"
    token = response.json().get("token")
    assert token, "No token returned from auth request"
    return token

@pytest.fixture
def create_booking(auth_token):
    """Fixture to create a booking and ensure cleanup after tests."""
    booking_ids = []

    def _create_booking(payload):
        headers = {"Cookie": f"token={auth_token}"}
        response = requests.post(f"{BASE_URL}/booking", json=payload, headers=headers)
        assert response.status_code == 200, f"Booking creation failed: {response.text}"
        booking_id = response.json().get("bookingid")
        assert booking_id, "No booking ID returned from creation"
        booking_ids.append(booking_id)
        return response

    yield _create_booking

    for booking_id in booking_ids:
        response = requests.get(f"{BASE_URL}/booking/{booking_id}", timeout=15)

        if response.status_code == 404:
            continue

        assert response.status_code == 200

        delete_response = requests.delete(
            f"{BASE_URL}/booking/{booking_id}",
            headers={"Cookie": f"token={auth_token}"},
            timeout=15
        )
        assert delete_response.status_code == 201
