import jwt


SECRET = "my-secret"


def create_token(user_id):

    return jwt.encode(
        {"user_id": user_id},
        SECRET,
        algorithm="HS256"
    )


def verify_token(token):

    return jwt.decode(
        token,
        SECRET
    )