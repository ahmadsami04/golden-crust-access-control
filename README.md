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



Task 4 - Report, Handover, and Live Deployment



Project Overview



Golden Crust Bakery's Flask application uses authentication and role-based access control to protect sensitive pages.



The application supports three roles: admin, staff, and customer.



\- "/admin" is restricted to administrators.

\- "/orders" is available to authenticated users.

\- Unauthenticated visitors are redirected to the login page when accessing protected routes.

\- Unauthorized customers receive HTTP 403 Forbidden when attempting to access "/admin".



Local Setup Instructions



1\. Clone the repository:

&#x20;

&#x20;  "git clone https://github.com/ahmadsami04/golden-crust-access-control.git"



2\. Navigate to the project directory:

&#x20;

&#x20;  "cd golden-crust-access-control"



3\. Create a virtual environment:

&#x20;

&#x20;  "python -m venv venv"



4\. Activate the environment on Windows using Git Bash:

&#x20;

&#x20;  "source venv/Scripts/activate"



5\. Install dependencies:

&#x20;

&#x20;  "pip install -r requirements.txt"



6\. Start the application:

&#x20;

&#x20;  "python app.py"



7\. Open the application in your browser:

&#x20;

&#x20;  "http://127.0.0.1:5000/login"



Security Testing



The project includes "test\_access.py", which demonstrates broken access control in an isolated vulnerable test application and verifies that the protected application returns HTTP 403 Forbidden for unauthorized customers.



To run the tests, start the Flask application in one terminal and run "python test\_access.py" in another terminal.



Deployment Preparation



The application will be configured for deployment using a "Procfile", a dependency file named "requirements.txt", and a production WSGI server.



Before deployment, the following security and configuration changes are required:



\- Replace the hardcoded Flask secret key with an environment variable.

\- Disable Flask debug mode in production.

\- Configure a production WSGI server such as Gunicorn.

\- Replace demonstration passwords with secure credentials.

\- Configure persistent database storage because Heroku's filesystem is ephemeral.

\- Verify all authentication and authorization routes on the deployed application.



Heroku Deployment Instructions



Once the application is configured for production and a Heroku account with a suitable plan is available:



1\. Install the Heroku CLI and authenticate using "heroku login".

2\. Create the Heroku application using "heroku create".

3\. Configure the required environment variables using "heroku config:set".

4\. Deploy the application using "git push heroku main".

5\. Check deployment logs using "heroku logs --tail".

6\. Open the application using "heroku open".

7\. Test the login page, "/admin", "/orders", and logout functionality.



Deployment Status: Not yet deployed. The live URL will be added after successful deployment and testing.



Audit Report



The security findings, fixes, test results, and future recommendations are documented in "AUDIT\_REPORT.md".



Project Repository



https://github.com/ahmadsami04/golden-crust-access-control

