class UserDataNotValid(Exception):
    def __init__(self, user_id, message="User data is not valid"):
        self.user_id = user_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} for user_id: {self.user_id}"


class NotificationError(Exception):
    def __init__(self, user_id, message="Notification error occurred"):
        self.user_id = user_id
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} for user_id: {self.user_id}"