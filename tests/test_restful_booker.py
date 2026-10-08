import pytest
import requests
from conftest import BASE_URL

def test_create_booking_returns_200(create_booking, booking_data):
    response = create_booking(booking_data)
    assert response.status_code == 200

def test_create_booking_returns_sent_data(create_booking, booking_data):
    response = create_booking(booking_data)
    assert response.json()["booking"] == booking_data

def test_get_by_id_returns_created_booking(create_booking, booking_data):
    created = create_booking(booking_data)
    booking_id = created.json()["bookingid"]

    response = requests.get(
        f"{BASE_URL}/booking/{booking_id}",
        timeout=15
    )

    assert response.status_code == 200
    assert response.json() == booking_data

def test_update_booking_saves_changed_firstname(create_booking, booking_data, auth_token):
    created = create_booking(booking_data)
    booking_id = created.json()["bookingid"]

    updated_data = {**booking_data, "firstname": "New"}
    headers = {"Cookie": f"token={auth_token}"}

    update_response = requests.put(
        f"{BASE_URL}/booking/{booking_id}",
        json=updated_data,
        headers=headers,
        timeout=15
    )
    assert update_response.status_code == 200

    response = requests.get(
        f"{BASE_URL}/booking/{booking_id}",
        timeout=15
    )

    assert response.status_code == 200
    assert response.json() == updated_data

def test_delete_booking_removes_booking(create_booking, booking_data, auth_token):
    created = create_booking(booking_data)
    booking_id = created.json()["bookingid"]
    delete_response = requests.delete(
        f"{BASE_URL}/booking/{booking_id}",
        headers={"Cookie": f"token={auth_token}"},
        timeout=15
    )

    assert delete_response.status_code == 201

    response = requests.get(
        f"{BASE_URL}/booking/{booking_id}",
        timeout=15
    )
    assert response.status_code == 404

def test_update_without_auth_returns_403(create_booking, booking_data):
    created = create_booking(booking_data)
    booking_id = created.json()["bookingid"]
    updated_data = {**booking_data, "firstname": "Unauthorized"}

    response = requests.put(
        f"{BASE_URL}/booking/{booking_id}",
        json=updated_data,
        timeout=15
    )

    assert response.status_code == 403, (
        f"Expected 403, got {response.status_code}: {response.text}"
    )

def test_missing_firstname_returns_client_error(booking_data):
    invalid_data = booking_data.copy()
    del invalid_data["firstname"]

    response = requests.post(
        f"{BASE_URL}/booking",
        json=invalid_data,
        timeout=15
    )
    assert 400 <= response.status_code < 500, (
        f"Expected a clean 4xx rejection, "
        f"got {response.status_code}: {response.text}"
    )

