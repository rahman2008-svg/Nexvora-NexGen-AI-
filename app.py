from flask import Flask, render_template, request, redirect, session, jsonify
from memory import save_qa, get_all
from brain import chat_ai, generate_smart_answer

app = Flask(__name__)
app.secret_key = "nexvora-secret"

# simple user storage (demo)
users = {}

# 🏠 Home
@app.route('/')
def home():
    if "user" not in session:
        return redirect("/login")
    return render_template("chat.html")


# 💬 Chat API
@app.route('/chat', methods=['POST'])
def chat():
    q = request.form['question']
    user = session.get("user", "guest")

    a = chat_ai(user, q)

    return jsonify({"answer": a})


# 🧠 Suggestion API (NEW 🔥)
@app.route('/suggest')
def suggest():
    return jsonify({
        "suggestion": "তুমি কি জানতে চাও — বাংলাদেশ, বিজ্ঞান, নাকি প্রযুক্তি?"
    })


# 📘 Teach AI
@app.route('/teach', methods=['GET', 'POST'])
def teach():
    if "user" not in session:
        return redirect("/login")

    if request.method == "POST":
        q = request.form['question']
        a = request.form['answer']
        save_qa(q, a)

    return render_template("teach.html")


# 📊 Dashboard
@app.route('/dashboard')
def dashboard():
    data = get_all()
    return render_template("dashboard.html", total=len(data))


# 🤖 Auto AI response
@app.route('/auto')
def auto():
    return jsonify({"ai": generate_smart_answer("random question")})


# 🧠 AI thinking
@app.route('/ai_think')
def ai_think():
    return jsonify({
        "thought": "তুমি কি আমাকে নতুন কিছু শেখাতে চাও? 😊"
    })


# 🔐 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        u = request.form['username']
        p = request.form['password']

        if u in users and users[u] == p:
            session['user'] = u
            return redirect("/")
    return render_template("login.html")


# 📝 Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == "POST":
        users[request.form['username']] = request.form['password']
        return redirect("/login")
    return render_template("register.html")


# 🚪 Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect("/login")


# ▶️ Run App
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
