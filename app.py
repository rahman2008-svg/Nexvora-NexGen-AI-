from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_bcrypt import Bcrypt
from tinydb import TinyDB, Query
from rapidfuzz import process
import os
import json

app = Flask(__name__)
app.secret_key = "secret123"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

bcrypt = Bcrypt(app)

# DB
user_db = TinyDB("users.json")
ai_db_file = "ai_memory.json"

if not os.path.exists(ai_db_file):
    with open(ai_db_file, "w") as f:
        json.dump([], f)

UserQuery = Query()

# User class
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    users = user_db.all()
    for u in users:
        if u["id"] == int(user_id):
            return User(u["id"], u["username"], u["password"])
    return None

# Routes
@app.route("/")
def home():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        hashed = bcrypt.generate_password_hash(password).decode("utf-8")

        users = user_db.all()
        user_id = len(users) + 1

        user_db.insert({
            "id": user_id,
            "username": username,
            "password": hashed
        })

        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        users = user_db.all()
        for u in users:
            if u["username"] == username and bcrypt.check_password_hash(u["password"], password):
                user = User(u["id"], u["username"], u["password"])
                login_user(user)
                return redirect(url_for("dashboard"))

        return "Wrong credentials"

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# Teach AI
@app.route("/teach", methods=["GET", "POST"])
@login_required
def teach():
    if request.method == "POST":
        q = request.form["question"]
        a = request.form["answer"]

        with open(ai_db_file, "r") as f:
            data = json.load(f)

        data.append({"q": q, "a": a})

        with open(ai_db_file, "w") as f:
            json.dump(data, f)

        return "Learned!"

    return render_template("teach.html")

# Chat AI
@app.route("/chat", methods=["GET", "POST"])
@login_required
def chat():
    if request.method == "POST":
        user_q = request.form["question"]

        with open(ai_db_file, "r") as f:
            data = json.load(f)

        questions = [item["q"] for item in data]

        if len(questions) > 0:
            match, score, index = process.extractOne(user_q, questions)

            if score > 60:
                return jsonify({"answer": data[index]["a"]})

        return jsonify({"answer": "I don't know yet. Teach me!"})

    return render_template("chat.html")

# Run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
