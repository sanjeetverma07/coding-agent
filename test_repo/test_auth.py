from auth import create_token
from app import authenticate


def test_authentication():

    token = create_token(123)

    user_id = authenticate(token)

    assert user_id == "123"