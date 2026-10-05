\# Golden Crust Access Control



This is a beginner Flask project created for Golden Crust Bakery. The purpose of the project is to build a basic login system and protect pages that should only be available to authenticated users.



\## What I Did



I created a Flask web application with a login page and a protected dashboard. User information is stored in a SQLite database. Passwords are hashed using Werkzeug instead of being stored as plain text.



I also used Flask-Login to manage user sessions. A user who is not logged in cannot directly access the dashboard and is redirected to the login page. After a successful login, the user can access the dashboard until they log out.



\## Technologies Used



\- Python

\- Flask

\- Flask-Login

\- SQLite

\- Werkzeug

\- Git

\- GitHub



\## How to Run the Project



Create and activate a Python virtual environment.



Install the required packages:



pip install -r requirements.txt



Run the application:



python app.py



Then open the login page in your browser:



http://127.0.0.1:5000/login



\## Testing



The application was tested for:



\- Successful login with correct credentials

\- Rejection of an incorrect password

\- Protection of the dashboard while logged out

\- Session persistence after login

\- Logout and removal of the authenticated session



\## Why I Built It



The goal of this task was to learn how authentication and basic access control work in a Flask application. It also helped me understand password hashing, sessions, protected routes, SQLite databases, and using Git and GitHub to manage a project.



\## Task 2 - Role-Based Access Control



I extended the user system to support three roles: admin, staff, and customer. The SQLite users table now includes a role field, and sample accounts were created for testing each role.



I created a custom role\_required decorator to control access based on the logged-in user's role. The /admin route is restricted to admin users, while non-admin users receive a 403 Forbidden response.



I also added an /orders route protected with Flask-Login. Any authenticated user can access the orders page, while users who are not logged in are redirected to the login page.



\### Task 2 Testing



\- Admin user can access /admin

\- Customer user receives 403 Forbidden when accessing /admin

\- Authenticated customer can access /orders

\- Logged-out user is redirected to login when accessing /orders

\- Admin, staff, and customer accounts can all authenticate successfully



\## Task 3 - Broken Access Control Testing



I tested the /admin route using a Python requests-based test while logged in as a customer.



\### Vulnerability Identified



In the vulnerable version, the /admin route only required the user to be logged in and did not verify the user's role. The customer account was therefore able to access /admin by entering the URL directly.



Before the fix:



\- Customer login succeeded

\- GET /admin returned HTTP 200

\- Customer could view the admin page



\### Fix and Verification



The /admin route is protected with a role check that requires the admin role. I re-ran the same requests-based test after the protection was applied.



After the fix:



\- Customer login succeeded

\- GET /admin returned HTTP 403 Forbidden

\- Customer could no longer access the admin page



The test confirms that authentication alone is not enough for sensitive routes. Authorization must also verify that the authenticated user has the required role.

