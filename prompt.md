Prompt
Context and Role
As a Full-Stack Web Developer specializing in modern educational platforms, you are responsible for designing and developing a production-ready Student Career & Placement Portal Website. The system must provide students with a centralized platform to manage academic progress, placement preparation, internships, projects, and career resources.
The website should maintain a responsive, secure, and user-friendly experience while ensuring efficient data handling and performance.
________________________________________
Objective
Develop a complete full-stack Student Career & Placement Portal Website that:
•	Helps students manage placement preparation. 
•	Allows students to track coding practice and project progress. 
•	Displays internship and job opportunities. 
•	Includes secure authentication and profile management. 
•	Stores and manages student data efficiently. 
________________________________________
UI Requirements
Landing Page
The website must include:
•	Hero Section 
o	Animated welcome banner 
o	Career-focused tagline 
o	“Get Started” button 
•	About Platform Section 
o	Brief explanation of portal features 
o	Interactive cards 
•	Skills Tracker Section 
o	Student skill progress visualization 
o	Progress bars for technologies 
•	Placement Resources Section 
o	Interview questions 
o	Resume tips 
o	Coding resources 
•	Internship & Job Section 
o	Display opportunities 
o	Application links 
•	Contact Section 
o	Student feedback/contact form 
Dashboard Requirements
After login:
Students should be able to:
•	View profile 
•	Add/update skills 
•	Upload projects 
•	Track placement preparation 
•	Save interview notes 
•	View internship opportunities 
UI Design Constraints
The layout must be:
•	Fully responsive (mobile, tablet, desktop) 
•	Clean and modern 
•	User-friendly navigation 
•	Accessible using semantic HTML 
•	Performance optimized 
________________________________________
Authentication Requirements
Implement secure authentication:
User Features
•	Student Registration 
•	Login/Logout 
•	Password validation 
•	Profile update 
Security Requirements
•	Password hashing 
•	CSRF protection 
•	Secure session handling 
•	Input validation 
________________________________________
Backend Requirements
Using Python Django:
Implement APIs and backend logic for:
Student Management
•	Register student 
•	Update profile 
•	Store skills 
•	Manage projects 
Placement Tracking
Students can:
•	Add completed topics 
•	Track interview preparation 
•	Store coding progress 
Contact Form
Include:
•	Name 
•	Email 
•	Subject 
•	Message 
Requirements:
•	Store submissions in SQLite 
•	Validate inputs 
•	Show success/error messages 
________________________________________
Database Requirements
Using SQLite, create tables/models for:
Student Model
•	Full Name 
•	Email 
•	Password 
•	College 
•	Skills 
•	Resume 
Project Model
•	Project Name 
•	Description 
•	Technology Used 
•	GitHub Link 
Placement Tracker Model
•	Topic Name 
•	Status 
•	Completion Date 
Contact Model
•	Name 
•	Email 
•	Message 
•	Timestamp 
________________________________________
Data Processing Requirements
Ensure:
•	Form validation : Checks if user input is correct (like required fields filled, valid data entered).
Used to prevent wrong or incomplete data from being saved.
•	XSS prevention : Protects the website from malicious scripts injected by users.
Used to keep user data and website safe from attacks.
•	SQL injection protection: Prevents attackers from manipulating database queries using harmful input.Used to secure database and protect student data.
•	Email format validation : Checks if email is in correct format (example: name@gmail.com).
Used to ensure only valid email addresses are accepted.
•	Sanitized inputs : Removes or cleans harmful or unwanted characters from user input.
Used to keep data safe and clean before storing in database.
Return structured responses for:
•	Success messages 
•	Validation errors 
•	Authentication failures 
________________________________________
Output Requirements
The final website should provide:
•	Responsive UI 
•	Secure login system 
•	Student dashboard 
•	Placement tracking system 
•	Internship/job section 
•	Contact system 
•	SQLite database integration 
•	Smooth user experience 
________________________________________
Error Handling & Documentation
Provide:
•	Proper frontend validation messages 
•	Backend error handling 
•	Structured Django responses 
•	Project documentation 
Include:
•	Folder structure 
•	Installation steps 
•	Database migration steps 
•	Environment setup 
•	Deployment instructions 
________________________________________
Performance Requirements
Ensure:
•	Fast page loading 
•	Optimized database queries 
•	Mobile responsiveness 
•	SEO-friendly structure 
•	Scalable backend design 
________________________________________
Technology Stack
Frontend
•	HTML 
•	CSS 
•	JavaScript 
Backend
•	Python Django 
Database
•	SQLite 
Frontend Technologies
1. HTML (HyperText Markup Language)
Why it is used:
HTML is used to create the structure of the website. It helps in designing pages like the landing page, login page, dashboard, profile page, internship section, and contact form.
Use in this project:
•	Creating navigation bar, forms, buttons, sections, and dashboard layout 
•	Building pages like: 
o	Home page 
o	Student registration/login page 
o	Student dashboard 
o	Internship & placement page 
o	Contact page 
Why chosen:
•	Simple and easy to organize webpage structure 
•	Supports semantic tags for better accessibility and SEO 
•	Works smoothly with CSS and JavaScript 
Example:
•	<form> for registration/login 
•	<section> for hero section 
•	<table> or cards for placement tracking 
________________________________________
2. CSS (Cascading Style Sheets)
Why it is used:
CSS is used to make the website beautiful, responsive, and user-friendly.
Use in this project:
•	Styling landing page and dashboard 
•	Creating responsive design for mobile, tablet, and desktop 
•	Designing: 
o	Hero banner 
o	Skill progress bars 
o	Cards for internship/job opportunities 
o	Buttons and animations 
Why chosen:
•	Makes UI modern and professional 
•	Improves user experience 
•	Helps maintain consistent design throughout the website 
Features used:
•	Flexbox/Grid layout 
•	Media queries for responsiveness 
•	Hover effects and animations 
Example:
•	Progress bars for student skills 
•	Attractive placement resource cards 
________________________________________
3. JavaScript
Why it is used:
JavaScript adds interactivity and dynamic behavior to the website.
Use in this project:
•	Form validation before submission 
•	Skill progress updates 
•	Dynamic dashboard interactions 
•	Showing success/error messages 
•	Interactive buttons and animations 
Why chosen:
•	Improves user experience 
•	Reduces page reloads 
•	Makes website more interactive 
Example:
•	Password validation during registration 
•	Real-time progress updates 
•	Contact form validation 
________________________________________
Backend Technology
Python + Django
Why it is used:
Django is the main backend framework used to handle business logic, authentication, database operations, and security.
Use in this project:
•	Student registration and login system 
•	Profile management 
•	Placement tracking 
•	Project upload management 
•	Internship/job data handling 
•	Contact form processing 
Why Django is chosen:
1. Built-in Authentication
Django provides secure:
•	Login 
•	Logout 
•	Registration 
•	Session handling 
This saves development time and improves security.
2. Strong Security Features
Django provides:
•	Password hashing 
•	CSRF protection 
•	SQL injection prevention 
•	XSS protection 
•	Secure sessions 
These are important because student data is stored.
3. Fast Development
Django follows MVT (Model View Template) architecture, making development organized and faster.
4. Easy Database Handling
Django ORM helps communicate with the database without writing complex SQL queries.
Example:
Instead of SQL:
SELECT * FROM students;
Django:
Student.objects.all()
5. Scalability
The project can later expand by adding:
•	Admin panel 
•	AI career recommendations 
•	Resume analyzer 
•	Placement notifications 
________________________________________
Database Technology
SQLite
Why it is used:
SQLite is used to store all student-related data in the database.
Use in this project:
Stores:
•	Student details 
•	Skills 
•	Projects 
•	Placement tracking 
•	Contact form submissions 
•	Internship information 
Tables/Models:
•	Student Model 
•	Project Model 
•	Placement Tracker Model 
•	Contact Model 
Why chosen:
1. Beginner Friendly
Easy to configure and works directly with Django.
2. No Separate Installation
Unlike MySQL or PostgreSQL, SQLite comes built into Django.
3. Lightweight
Perfect for:
•	College projects 
•	Small to medium applications 
•	Fast development 
4. Easy Database Management
Django migrations automatically create tables.
Example:
python manage.py makemigrations
python manage.py migrate
