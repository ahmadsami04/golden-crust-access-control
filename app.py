import os
from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash,  check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ["SECRET_KEY"]
DATABASE_PATH = os.environ.get("DATABASE_PATH", "users.db")
DATABASE_ABSOLUTE_PATH = os.path.abspath(DATABASE_PATH)
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL", "sqlite:///" + DATABASE_ABSOLUTE_PATH.replace("\\", "/")
)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

class User(UserMixin):
    def __init__(self, id, username, role):
        self.id = str(id)
        self.username = username
        self.role = role
class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(50), nullable=False, default="customer")

def role_required(required_role):
    def decorator(function):
        @wraps(function)
        def wrapped_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return redirect(url_for("login"))

            if current_user.role != required_role:
                return "Forbidden", 403

            return function(*args, **kwargs)

        return wrapped_function

    return decorator


@login_manager.user_loader
def load_user(user_id):
    try:
        user_id = int(user_id)
    except (ValueError, TypeError):
        return None

    user = db.session.get(UserModel, user_id)

    if user is not None:
        return User(user.id, user.username, user.role)

    return None



def init_db():
    with app.app_context():
        db.create_all()

        if os.environ.get("ENABLE_DEMO_USERS") == "1":
            sample_users = [
                ("admin", "bakery123", "admin"),
                ("staff", "staff123", "staff"),
                ("customer", "customer123", "customer"),
            ]

            for username, password, role in sample_users:
                user = UserModel.query.filter_by(
                    username=username
                ).first()

                if user is None:
                    user = UserModel(
                        username=username,
                        password=generate_password_hash(password),
                        role=role,
                    )
                    db.session.add(user)

            db.session.commit()


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        user = UserModel.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            logged_in_user = User(user.id, user.username, user.role)
            login_user(logged_in_user)
            return redirect(url_for("dashboard"))

        return "Invalid username or password"

    return render_template("login.html")

@app.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html")

@app.route("/admin")
@role_required("admin")
def admin():
    return "Golden Crust Bakery - Admin Page"

@app.route("/orders")
@login_required
def orders():
    return "Golden Crust Bakery - Orders Page"

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

if __name__ == "__main__":
    init_db()
    app.run(debug=False)