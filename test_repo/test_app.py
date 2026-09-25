import pytest

from app import login, authenticate
from auth import create_token, verify_token


def test_login_success():
    """Login with correct credentials should return a valid JWT token."""
    token = login("admin", "secret")
    # The token should be decodable and contain the correct user_id
    payload = verify_token(token)
    assert payload["user_id"] == "admin"


def test_login_invalid_credentials():
    """Login with wrong credentials should raise a ValueError."""
    with pytest.raises(ValueError):
        login("admin", "wrong")


def test_authenticate_function():
    """authenticate should return the user_id as a string from a token."""
    token = create_token(123)
    user_id = authenticate(token)
    assert user_id == "123"
