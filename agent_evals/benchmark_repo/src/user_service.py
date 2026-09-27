class UserService:

    def __init__(self):
        self.users = {}

    def create_user(self, user_id, name):
        self.users[user_id] = {
            "id": user_id,
            "name": name
        }

        return self.users[user_id]

    def get_user(self, user_id):
        return self.users.get(user_id)