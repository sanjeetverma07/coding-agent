from src.user_service import UserService


def test_create_user():

    service = UserService()

    user = service.create_user(
        1,
        "Sanjeet"
    )

    assert user["id"] == 1
    assert user["name"] == "Sanjeet"


def test_get_user():

    service = UserService()

    service.create_user(
        1,
        "Sanjeet"
    )

    user = service.get_user(1)

    assert user["name"] == "Sanjeet"


def test_missing_user():

    service = UserService()

    assert service.get_user(999) is None