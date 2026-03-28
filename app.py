from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from tinydb import TinyDB, Query
import json
import os

# ---------------- Flask App Setup ----------------
app = Flask(__name__)
app.secret_key = "YOUR_SECRET_KEY"  # Change this to something secure

# ---------------- Flask Login Setup ----------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

bcrypt = Bcrypt(app)

# ---------------- Database Setup ----------------
db_file = "users.json"
if not os.path.exists(db_file):
    with open(db_file, "w") as f:
        json.dump([], f)

ai_memory_file = "ai_memory.json"
if not os.path.exists(ai_memory_file):
    with open(ai_memory_file, "w") as f:
        json.dump({}, f)

db = TinyDB(db_file)
UserQuery = Query()

# ---------------- User Class ----------------
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    users = db.all()
    for u in users:
        if u["id"] == int(user_id):
            return User(u["id"], u["username"], u["password"])
    return None

# ---------------- Routes ----------------
@app.route("/")
def home():
    return redirect(url_for("dashboard"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed_pw = bcrypt.generate_password_hash(password).decode("utf-8")

        users = db.all()
        if any(u["username"] == username for u in users):
            return "Username already exists!"
        
        user_id = len(users) + 1
        db.insert({"id": user_id, "username": username, "password": hashed_pw})
        return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        users = db.all()
        for u in users:
            if u["username"] == username and bcrypt.check_password_hash(u["password"], password):
                user = User(u["id"], u["username"], u["password"])
                login_user(user)
                return redirect(url_for("dashboard"))
        return "Invalid username or password!"
    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

# ---------------- AI Teach / Chat ----------------
@app.route("/teach", methods=["GET", "POST"])
@login_required
def teach():
    if request.method == "POST":
        question = request.form.get("question")
        answer = request.form.get("answer")
        with open(ai_memory_file, "r") as f:
            memory = json.load(f)
        memory[question] = answer
        with open(ai_memory_file, "w") as f:
            json.dump(memory, f, indent=4)
        return jsonify({"status": "success", "message": "Question learned!"})
    return render_template("teach.html")

@app.route("/chat", methods=["POST"])
@login_required
def chat():
    user_question = request.form.get("question")
    with open(ai_memory_file, "r") as f:
        memory = json.load(f)
    
    # Simple exact-match AI
    answer = memory.get(user_question, "এখনও এই প্রশ্ন শেখানো হয়নি।")
    return jsonify({"answer": answer})

# ---------------- Run App ----------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
