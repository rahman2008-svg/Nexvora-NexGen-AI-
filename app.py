from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt
from tinydb import TinyDB, Query
import brain, memory, utils

app = Flask(__name__)
app.secret_key = "supersecretkey"

bcrypt = Bcrypt(app)
login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)

# TinyDB for users
db_users = TinyDB('users.json')
UserQuery = Query()

class User(UserMixin):
    def __init__(self, id, email, password):
        self.id = id
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    result = db_users.get(UserQuery.id == int(user_id))
    if result:
        return User(result['id'], result['email'], result['password'])
    return None

@app.route('/')
def home():
    return redirect(url_for('login'))

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        user_id = len(db_users.all()) + 1
        db_users.insert({'id': user_id, 'name': name, 'email': email, 'password': password})
        return redirect(url_for('login'))
    return render_template('register.html')

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = db_users.get(UserQuery.email == email)
        if user and bcrypt.check_password_hash(user['password'], password):
            login_user(User(user['id'], user['email'], user['password']))
            return redirect(url_for('dashboard'))
        else:
            return "Invalid Credentials"
    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Dashboard
@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Chat API
@app.route('/chat', methods=['POST'])
@login_required
def chat():
    data = request.get_json()
    question = data.get('question')
    answer = brain.get_answer(question)
    return jsonify({'answer': answer})

# Teach AI API
@app.route('/teach', methods=['POST'])
@login_required
def teach():
    data = request.get_json()
    question = data.get('question')
    answer = data.get('answer')
    memory.add_knowledge(question, answer)
    return jsonify({'message': 'AI শেখানো হয়েছে!'})

# Suggestion
@app.route('/suggest')
@login_required
def suggest():
    return jsonify({"suggestion": "তুমি কি জানতে চাও — বাংলাদেশ, বিজ্ঞান, নাকি প্রযুক্তি?"})

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
