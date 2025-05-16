from src.shared.domain.entities.booking import Booking


class UserViewModel:
    user_id: str
    name: str

    def __init__(self, user_id: str, name: str):
        self.user_id = user_id
        self.name = name

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'name': self.name
        }

class GetAllUsersViewModel:
    users: list[UserViewModel]

    def __init__(self, users: list[dict]):
        self.users = [UserViewModel(user["user_id"], user["name"]) for user in users]

    def to_dict(self):
        return {
            'users': [user.to_dict() for user in self.users],
            'message': 'the users were retrieved'
        }