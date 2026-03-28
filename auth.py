from tinydb import TinyDB

users_db = TinyDB("users.json")

def get_user(username):
    User = users_db.search
    results = users_db.search(lambda u: u["username"] == username)
    return results[0] if results else None
