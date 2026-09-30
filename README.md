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

