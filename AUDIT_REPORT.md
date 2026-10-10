Golden Crust Bakery - Access Control Security Audit Report



Project: Access Control Review for Golden Crust Bakery

Prepared by: Ahmad Sami

Technology: Python, Flask, Flask-Login, SQLite

Date: October 2026



1\. Introduction



The purpose of this security audit was to review the authentication and authorization system of Golden Crust Bakery's web application. The main goal was to identify broken access control vulnerabilities, implement role-based access restrictions, and verify that unauthorized users could not access sensitive pages.



2\. Vulnerability Identified



The main security issue was broken access control affecting the "/admin" route.



In a deliberately recreated vulnerable version of the application, the admin page required a user to be logged in but did not verify whether the user had administrator privileges.



This allowed an authenticated customer to access the admin page directly by entering "/admin" in the browser.



The vulnerability demonstrated why authentication alone is insufficient to protect sensitive application resources.



3\. Security Fix Implemented



Role-based access control was implemented using Flask-Login and a custom "role\_required" decorator.



The application supports three user roles:



\- Admin: Authorized to access the admin page.

\- Staff: Can log in and access general authenticated pages.

\- Customer: Can log in and access general authenticated pages.



The "/admin" route requires the administrator role. Non-admin users receive HTTP 403 Forbidden.



The "/orders" route requires authentication, allowing logged-in users to access it while redirecting unauthenticated visitors to the login page.



User passwords are stored as hashes using Werkzeug rather than plaintext.



4\. Security Testing and Results



A Python "requests"-based test was created to evaluate the access-control behavior.



Before-Fix Demonstration



A deliberately vulnerable test application was run separately from the protected application.



\- Customer login succeeded.

\- The customer requested "/admin".

\- The server returned HTTP 200 OK.

\- The customer could access the admin page.



Result: The isolated demonstration reproduced broken access-control behavior.



After-Fix Verification



The test was repeated against the protected Flask application.



\- Customer login succeeded.

\- The customer requested "/admin".

\- The server returned HTTP 403 Forbidden.

\- The customer was prevented from accessing the admin page.



Result: The authorization check successfully blocked the customer.



5\. Recommendations



To improve the application's security further, the following actions are recommended:



\- Use strong, unique passwords and remove demonstration credentials before production deployment.

\- Store Flask secret keys in environment variables rather than directly in the source code.

\- Disable Flask debug mode in production.

\- Add CSRF protection to forms that modify application state.

\- Apply secure session-cookie settings and HTTPS.

\- Implement login rate limiting to reduce brute-force attacks.

\- Continue automated authorization testing whenever protected routes are modified.

\- Use persistent database storage, backups, and appropriate database permissions for production deployment.



6\. Conclusion



The access-control review demonstrated how an authenticated customer could reach a sensitive admin page when authorization checks were missing.



The protected application now restricts "/admin" to administrators and requires authentication for "/orders".



Testing confirmed that the deliberately vulnerable test returned HTTP 200, while the protected application returned HTTP 403 Forbidden for the same customer account.



The project demonstrates the importance of enforcing authorization checks on the server side and regularly testing access restrictions.



7\. Project Repository



GitHub Repository: https://github.com/ahmadsami04/golden-crust-access-control



Deployment Status: Pending live deployment and verification.
