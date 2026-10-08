"""Restful-booker DeleteBooking tests.

Source: https://restful-booker.herokuapp.com/apidoc/index.html
DELETE success: 201, following the response example despite 'Success 200'.
Assumptions requiring confirmation: unauthenticated DELETE = 403;
GET after deletion = 404. Neither error status is specified in the docs.
"""
import pytest
import requests

BASE_URL = "https://restful-booker.herokuapp.com"
TIMEOUT = 15


@pytest.fixture
def client():
    # Avoid implicit .netrc authentication and inherited proxy credentials.
    with requests.Session() as session:
        session.trust_env = False
        yield session

@pytest.fixture
def auth_token(client):
    response = client.post(
        f"{BASE_URL}/auth",
        json={"username": "admin", "password": "password123"},
        timeout=TIMEOUT,
        allow_redirects=False,
    )
    assert response.status_code == 200, (
        f"Auth expected 200, got {response.status_code}: {response.text}"
    )
    token = response.json().get("token")
    assert isinstance(token, str) and token, "Auth response has no usable token"
    return token


@pytest.fixture
def booking(client, auth_token):
    # Default fixture scope is function: each test gets a new booking.
    original = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-11-01", "checkout": "2026-11-03"},
        "additionalneeds": "Breakfast",
    }
    response = client.post(
        f"{BASE_URL}/booking",
        json=original,
        headers={"Accept": "application/json"},
        timeout=TIMEOUT,
        allow_redirects=False,
    )
    assert response.status_code == 200, (
        f"Create expected 200, got {response.status_code}: {response.text}"
    )
    booking_id = response.json().get("bookingid")
    assert type(booking_id) is int, "Create response has no integer bookingid"
    url = f"{BASE_URL}/booking/{booking_id}"

    try:
        assert response.json().get("booking") == original, (
            "Created booking does not match the submitted data"
        )
        yield url, original
    finally:
        # Pytest reports teardown errors separately, preserving test failures.
        remaining = client.get(
            url, headers={"Accept": "application/json"},
            timeout=TIMEOUT, allow_redirects=False,
        )
        if remaining.status_code != 404:
            cleanup = client.delete(
                url, headers={"Cookie": f"token={auth_token}"},
                timeout=TIMEOUT, allow_redirects=False,
            )
            assert cleanup.status_code == 201, (
                f"Cleanup DELETE expected 201, got {cleanup.status_code}: "
                f"{cleanup.text} (booking {booking_id})"
            )
            check = client.get(
                url, headers={"Accept": "application/json"},
                timeout=TIMEOUT, allow_redirects=False,
            )
            assert check.status_code == 404, (
                f"Cleanup GET expected 404 (assumption), got {check.status_code}: "
                f"{check.text} (booking {booking_id})"
            )


def test_delete_booking_with_token(client, auth_token, booking):
    url, _ = booking
    response = client.delete(
        url, headers={"Cookie": f"token={auth_token}"},
        timeout=TIMEOUT, allow_redirects=False,
    )
    assert response.status_code == 201, (
        f"DELETE expected documented example status 201, got "
        f"{response.status_code}: {response.text}"
    )
    response = client.get(
        url, headers={"Accept": "application/json"},
        timeout=TIMEOUT, allow_redirects=False,
    )
    assert response.status_code == 404, (
        f"GET after deletion expected 404 (assumption requiring confirmation), "
        f"got {response.status_code}: {response.text}"
    )


def test_delete_booking_without_auth(client, booking):
    url, original = booking
    # A separate session sends neither the token nor Basic authentication.
    with requests.Session() as anonymous:
        anonymous.trust_env = False
        response = anonymous.delete(
            url, timeout=TIMEOUT, allow_redirects=False,
        )
    assert response.status_code == 403, (
        f"Unauthenticated DELETE expected 403 (assumption requiring confirmation), "
        f"got {response.status_code}: {response.text}"
    )
    response = client.get(
        url, headers={"Accept": "application/json"},
        timeout=TIMEOUT, allow_redirects=False,
    )
    assert response.status_code == 200, (
        f"Booking should still exist: GET expected 200, got "
        f"{response.status_code}: {response.text}"
    )
    assert response.json() == original, (
        f"Booking changed after rejected DELETE: {response.json()}"
    )
