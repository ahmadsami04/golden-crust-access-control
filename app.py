from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user

app = Flask(__name__)
app.secret_key = "golden-crust-secret-key"

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = str(id)
        self.username = username
        self.role = role

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, username, role FROM users WHERE id = ?",
        (user_id,)
    )
    user = cursor.fetchone()
    conn.close()

    if user:
        return User(user[0], user[1], user[2])

    return None

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
       CREATE TABLE IF NOT EXISTS users (
           id INTEGER PRIMARY KEY AUTOINCREMENT,
           username TEXT NOT NULL UNIQUE,
           password TEXT NOT NULL,
           role TEXT NOT NULL DEFAULT 'customer'
        )
    """)

    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in
    cursor.fetchall()]

    if "role" not in columns:
        cursor.execute(
             "ALTER TABLE users ADD COLUMN role TEXT NOT NULL DEFAULT 'customer'"
        )

    cursor.execute("SELECT * FROM users WHERE username = ?", ("admin",))
    user = cursor.fetchone()

    if user is None:
        hashed_password = generate_password_hash("bakery123")
        cursor.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            ("admin", hashed_password)
        )
    cursor.execute(
        "UPDATE users SET role = ? WHERE username = ?",
        ("admin" , "admin")
    )
    sample_users = [
        ("staff", "staff123", "staff"),
        ("customer", "customer123", "customer")
    ]
     
    for username, password, role in sample_users:
         cursor.execute(
             "SELECT * FROM users WHERE username = ?",
             (username,)
         )
        
         if cursor.fetchone() is None: 
             hashed_password = generate_password_hash(password)
             cursor.execute(
                 "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                 (username, hashed_password, role)
             )

    conn.commit()
    conn.close()

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        )
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user[2], password):
            logged_in_user = User(user[0], user[1], user[3])
            login_user(logged_in_user)
            return redirect(url_for("dashboard"))

        return "Invalid username or password"

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

if __name__ == "__main__":
    init_db()
    app.run(debug=True)