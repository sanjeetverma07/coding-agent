import pytest

from app import login, authenticate, register
from auth import create_token, verify_token


def test_login_success():
    """Login with correct credentials should return a valid JWT token."""
    # Register user first
    register("admin", "secret")
    token = login("admin", "secret")
    # The token should be decodable and contain the correct user_id
    payload = verify_token(token)
    assert payload["user_id"] == "admin"


def test_login_invalid_credentials():
    """Login with wrong credentials should raise a ValueError."""
    # Ensure user exists
    register("admin2", "secret2")
    with pytest.raises(ValueError):
        login("admin2", "wrong")


def test_authenticate_function():
    """authenticate should return the user_id as a string from a token."""
    token = create_token(123)
    user_id = authenticate(token)
    assert user_id == "123"


def test_register_success():
    """Register a new user and then login successfully."""
    register("newuser", "newpass")
    token = login("newuser", "newpass")
    payload = verify_token(token)
    assert payload["user_id"] == "newuser"


def test_register_duplicate():
    """Registering an existing username should raise ValueError."""
    register("dupuser", "pass")
    with pytest.raises(ValueError):
        register("dupuser", "other")
