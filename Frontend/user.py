from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, email, name):
        self.email = email
        self.name = name

    def get_id(self):
        return self.email
