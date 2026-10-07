import requests
from flask import Flask, request, redirect
from threading import Thread
from werkzeug.serving import make_server

REAL_URL = "http://127.0.0.1:5000"
TEST_URL = "http://127.0.0.1:5001"

# --------------------------------------------------
# BEFORE FIX
# Reproduce the original broken access-control design
# in an isolated test server.
# --------------------------------------------------

vulnerable_app = Flask(__name__)
logged_in_users = set()


@vulnerable_app.route("/login", methods=["POST"])
def vulnerable_login():
    username = request.form.get("username")
    password = request.form.get("password")

    if username == "customer" and password == "customer123":
        logged_in_users.add(username)
        return redirect("/dashboard")

    return "Invalid username or password", 401


@vulnerable_app.route("/dashboard")
def vulnerable_dashboard():
    return "Customer Dashboard"


@vulnerable_app.route("/admin")
def vulnerable_admin():
    # BEFORE FIX: no role check was performed.
    return "Golden Crust Bakery - Admin Page", 200


server = make_server("127.0.0.1", 5001, vulnerable_app)
thread = Thread(target=server.serve_forever)
thread.daemon = True
thread.start()

before_session = requests.Session()

before_login = before_session.post(
    f"{TEST_URL}/login",
    data={
        "username": "customer",
        "password": "customer123"
    }
)

before_admin = before_session.get(
    f"{TEST_URL}/admin",
    allow_redirects=False
)

print("--- BEFORE FIX TEST ---")
print("Customer login status:", before_login.status_code)
print("Admin page status:", before_admin.status_code)
print("Admin page response:", before_admin.text)

if before_admin.status_code == 200:
    print("VULNERABILITY CONFIRMED: Customer could access /admin before the fix.")
else:
    print("FAIL: Before-fix vulnerability was not reproduced.")

server.shutdown()


# --------------------------------------------------
# AFTER FIX
# Test the real application with role protection.
# --------------------------------------------------

after_session = requests.Session()

after_login = after_session.post(
    f"{REAL_URL}/login",
    data={
        "username": "customer",
        "password": "customer123"
    }
)

after_admin = after_session.get(
    f"{REAL_URL}/admin",
    allow_redirects=False
)

print("\n--- AFTER FIX TEST ---")
print("Customer login status:", after_login.status_code)
print("Admin page status:", after_admin.status_code)
print("Admin page response:", after_admin.text)

if after_admin.status_code == 403:
    print("PASS: Customer is blocked from /admin after the fix.")
else:
    print("FAIL: Customer can still access /admin.")