from auth import verify_token, create_token

# Simple in-memory user store: username -> password
_USERS = {}

def authenticate(token):
    """Verify a JWT token and return the user_id as a string."""
    payload = verify_token(token)
    return str(payload["user_id"])

def register(username: str, password: str) -> None:
    """Register a new user. Raises ValueError if username already exists."""
    if username in _USERS:
        raise ValueError("User already exists")
    _USERS[username] = password

def login(username: str, password: str) -> str:
    """Login function that returns a JWT token for valid credentials.

    Checks credentials against the in‑memory user store.
    """
    stored_password = _USERS.get(username)
    if stored_password is None or stored_password != password:
        raise ValueError("Invalid credentials")
    # Use the username as the user identifier in the token
    return create_token(username)
