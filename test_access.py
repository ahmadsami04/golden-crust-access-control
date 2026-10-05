import requests
BASE_URL = "http://127.0.0.1:5000"

session = requests.Session()

login_data = {
    "username": "customer",
    "password": "customer123"
}

login_response = session.post(
    f"{BASE_URL}/login",
    data=login_data
)

print("Login status:", login_response.status_code)

admin_response = session.get(
    f"{BASE_URL}/admin",
    allow_redirects=False
)

print("Admin page status:", admin_response.status_code)
print("Admin page response:", admin_response.text)

if admin_response.status_code == 403:
    print("PASS: Customer was blocked from /admin.")
else:
    print("FAIL: Customer was able to access /admin.")