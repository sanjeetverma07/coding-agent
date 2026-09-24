from auth import verify_token


def authenticate(token):

    payload = verify_token(token)

    return str(payload["user_id"])