from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.name = "user" + str(user_id)
        self.password = self.name + "_secret"
        self.email = "hello_%s@world.com" % self.name
        
    def __repr__(self):
        return "%d/%s/%s/%s" % (self.user_id, self.name, self.password, self.email)

    def get_id(self):
        return self.user_id