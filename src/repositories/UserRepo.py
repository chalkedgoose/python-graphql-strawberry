from src.models.User import User

# Repository for interacting with user data.


class UserRepo:

    def get_users(self):
        return [
            User("Carlos", age=22),
            User("Haley", age=21),
            User("Charles", age=20),
            User("Shadi", age=20)
        ]
