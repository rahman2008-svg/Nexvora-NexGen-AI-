from flask_login import LoginManager, UserMixin
from memory import db_users

login_manager = LoginManager()
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = id
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    user = db_users.get(doc_id=int(user_id))
    if user:
        return User(user.doc_id, user['username'], user['role'])
    return None
