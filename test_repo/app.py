from auth import verify_token, create_token


def authenticate(token):
    """Verify a JWT token and return the user_id as a string."""
    payload = verify_token(token)
    return str(payload["user_id"])


def login(username: str, password: str) -> str:
    """Simple login function that returns a JWT token for valid credentials.

    For demonstration purposes, this uses a hard‑coded credential check.
    In a real application, you would verify the username and password
    against a user database.
    """
    # Hard‑coded example credentials
    if username == "admin" and password == "secret":
        # Use the username as the user identifier in the token
        return create_token(username)
    raise ValueError("Invalid credentials")