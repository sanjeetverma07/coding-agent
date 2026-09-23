from auth import verify_token


def authenticate(token):

    payload = veren(token)

    return payload["user_id"]