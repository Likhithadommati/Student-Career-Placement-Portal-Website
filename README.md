# Student Career & Placement Portal

A polished Django web application for students to manage career planning, placement preparation, projects, interview practice, and learning resources.

## What this project offers

- Student registration, login, and profile management
- Resume upload, project portfolio, and skill tracking
- Placement preparation tracker and interview note system
- Job/internship listings with application tracking
- Admin dashboard for managing users, resources, and opportunities
- Secure form handling, validation, and sanitization

## Key Features

### Student experience
- Account registration and secure authentication
- Personalized dashboard with quick access to key tools
- Profile editing, resume upload, and photo support
- Add and manage skills with proficiency levels
- Publish and present project entries with GitHub links
- Browse and apply for internships and placements
- Save interview notes and review practice questions
- Access curated resources and career guidance

### Admin experience
- Django admin interface for managing site data
- Control student profiles, job listings, interview notes, and resources
- Review contact form submissions and feedback

### Security & reliability
- Django authentication with password hashing
- CSRF protection on all form submissions
- SQL injection defense via Django ORM
- XSS protection using `bleach` sanitization
- Input validation for email, text, and file uploads
- Role-based access control for users and admins

## Technology Stack

- Python 3.8+
- Django 4.2
- SQLite (development default)
- HTML5, CSS3, Bootstrap 5
- JavaScript and Chart.js
- `bleach`, `python-decouple`, `Pillow`, `email-validator`

## Setup Instructions

> The Django project files are located in `GoldenResponse/Student Career`.

### 1. Open project directory
```bash
cd "GoldenResponse/Student Career"
```

### 2. Create and activate a virtual environment

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure environment variables
Create a `.env` file in the same folder as `manage.py` with:
```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=*
```

### 5. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a superuser
```bash
python manage.py createsuperuser
```

### 7. Collect static files
```bash
python manage.py collectstatic --noinput
```

### 8. Optional: load sample data
```bash
python manage.py loaddata initial_data
```

### 9. Start the development server
```bash
python manage.py runserver
```

Open `http://127.0.0.1:8000/` in your browser.

## Usage Guide

### For students
1. Register and log in
2. Complete your profile, upload your resume, and add skills
3. Add project entries and link GitHub repositories
4. Track placement preparation topics and progress
5. Review interview questions and save notes
6. Browse opportunities and apply for jobs or internships
7. Use the resources page for curated learning material

### For administrators
1. Visit `http://127.0.0.1:8000/admin/`
2. Sign in with the superuser account
3. Manage students, job listings, interview notes, and resources
4. Review contact submissions and student activity

## Project Layout

```
GoldenResponse/Student Career/
├── career_portal/                 # Main Django project settings
│   ├── __init__.py
│   ├── settings.py               # Django configuration
│   ├── urls.py                   # Main URL routing
│   ├── wsgi.py                   # WSGI application
│   └── asgi.py
│
├── portal/                        # Main Django application
│   ├── migrations/                # Database migrations
│   ├── __init__.py
│   ├── admin.py                  # Django admin configuration
│   ├── apps.py                   # App configuration
│   ├── models.py                 # Database models
│   ├── forms.py                  # Django forms with validation
│   ├── views.py                  # View functions
│   ├── urls.py                   # App-specific URL routing
│   └── tests.py
│
├── templates/                     # HTML templates
│   ├── base.html                 # Base template
│   └── portal/
│       ├── index.html            # Landing page
│       ├── register.html         # Registration
│       ├── login.html            # Login
│       ├── dashboard.html        # Dashboard
│       ├── profile.html          # Profile management
│       ├── skills.html           # Skills display
│       ├── projects.html         # Projects list
│       ├── opportunities.html    # Job listings
│       ├── contact.html          # Contact form
│       ├── 404.html              # Error page
│       └── ...
│
├── static/                        # Static files
│   ├── css/
│   │   └── style.css             # Custom CSS styling
│   ├── js/
│   │   └── main.js               # JavaScript interactions
│   └── images/
│
├── media/                         # User uploads
│   ├── profiles/                 # Profile pictures
│   ├── resumes/                  # Resume documents
│   ├── projects/                 # Project images
│   └── companies/                # Company logos
│
├── manage.py                      # Django management script
├── requirements.txt               # Python dependencies
├── README.md                      # This file
├── .env                          # Environment variables (not in repo)
└── db.sqlite3                    # Database file
```

## Database Models

### Student
- Full name, email, phone, roll number
- College, department, semester, CGPA
- Profile picture, resume, bio
- Timestamps

### Skill
- Skill name, proficiency level
- Years of experience, endorsements
- Associated with Student

### Project
- Project name, description, technologies used
- GitHub and live links, project image
- Start/end dates, completion status
- Associated with Student

### PlacementTracker
- Topic name, category (DSA, Web, ML, etc.)
- Status (Not Started, In Progress, Completed, Reviewed)
- Completion percentage, notes
- Resource links
- Associated with Student

### InterviewQuestion
- Question text, answer, category
- Difficulty level, company name
- Community database

### InterviewNotes
- Student's custom answer, review status
- Associated with InterviewQuestion and Student

### Opportunity
- Job/Internship title, company, description
- Location, salary range, required skills
- Application deadline, job link
- Company logo

### StudentApplication
- Application status tracking
- Associated with Student and Opportunity

### ContactForm
- Name, email, phone, subject, message
- Resolution status and response
- Timestamps

### Resource
- Title, description, URL
- Resource type (Article, Video, Course, etc.)
- Category

## API Endpoints

### Authentication
- `POST /register/` - Student registration
- `POST /login/` - Student login
- `GET /logout/` - Logout

### Dashboard
- `GET /dashboard/` - View dashboard

### Profile Management
- `GET /profile/` - View profile
- `POST /profile/` - Update profile

### Skills
- `GET /skills/` - List all skills
- `POST /skills/add/` - Add new skill
- `POST /skills/edit/<id>/` - Edit skill
- `GET /skills/delete/<id>/` - Delete skill

### Projects
- `GET /projects/` - List all projects
- `POST /projects/add/` - Add new project
- `POST /projects/edit/<id>/` - Edit project
- `GET /projects/delete/<id>/` - Delete project

### Placement Tracking
- `GET /placement-tracker/` - View tracker
- `POST /placement-tracker/add/` - Add topic
- `POST /placement-tracker/edit/<id>/` - Edit topic
- `GET /placement-tracker/delete/<id>/` - Delete topic

### Interview Preparation
- `GET /interview-prep/` - View questions
- `GET /interview-notes/` - View notes
- `POST /interview-notes/add/` - Add note
- `POST /interview-notes/edit/<id>/` - Edit note
- `GET /interview-notes/delete/<id>/` - Delete note

### Opportunities
- `GET /opportunities/` - List opportunities
- `GET /opportunities/<id>/` - View details
- `POST /opportunities/<id>/apply/` - Apply for opportunity
- `GET /my-applications/` - View applications

### Resources
- `GET /resources/` - List resources

### Contact
- `POST /contact/` - Submit contact form

## Security Considerations

### For Production Deployment

1. **Settings Updates**:
   ```python
   DEBUG = False
   SECRET_KEY = 'use-a-strong-random-key'
   ALLOWED_HOSTS = ['yourdomain.com']
   CSRF_COOKIE_SECURE = True
   SESSION_COOKIE_SECURE = True
   ```

2. **Database**: Migrate from SQLite to PostgreSQL or MySQL
   ```bash
   # Install PostgreSQL adapter
   pip install psycopg2-binary
   
   # Update DATABASES in settings.py
   ```

3. **SSL/HTTPS**: Configure HTTPS with proper certificates

4. **Static Files**: Use a CDN or separate web server

5. **Environment Variables**: Use `.env` file for sensitive data

6. **Email Configuration**: Configure email backend for notifications

7. **Backup Strategy**: Implement regular database backups

## Performance Optimization

1. **Database Queries**:
   - Use `select_related()` and `prefetch_related()`
   - Add database indexes on frequently queried fields

2. **Caching**:
   - Implement Redis for session storage
   - Cache static resources

3. **Frontend**:
   - Minify CSS and JavaScript
   - Optimize images
   - Enable GZIP compression

4. **Server**:
   - Use Gunicorn or uWSGI as application server
   - Configure Nginx as reverse proxy
   - Implement rate limiting

## Troubleshooting

### Issue: Migration errors
```bash
# Reset migrations (development only)
python manage.py migrate zero
python manage.py makemigrations
python manage.py migrate
```

### Issue: Static files not loading
```bash
python manage.py collectstatic --clear --noinput
```

### Issue: Database locked
```bash
# Delete temporary database files and recreate
rm db.sqlite3
python manage.py migrate
```

### Issue: Template not found
- Check template path in `settings.py`
- Verify `APP_DIRS = True` in TEMPLATES configuration

## Deployment Options

### Option 1: Heroku
1. Install Heroku CLI
2. Create Procfile and runtime.txt
3. Deploy: `git push heroku main`

### Option 2: DigitalOcean / AWS
1. Set up server with Python and Django requirements
2. Use Gunicorn and Nginx
3. Configure SSL with Let's Encrypt

### Option 3: PythonAnywhere
1. Create account on PythonAnywhere
2. Upload project files
3. Configure web app settings

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a feature branch
3. Make changes and test
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues, questions, or suggestions:
- Email: support@careerhub.edu
- GitHub Issues: [Repository Issues]

## Version History

### v1.0.0 (Initial Release)
- Complete student portal functionality
- Placement tracking system
- Interview preparation module
- Job/Internship tracking
- Secure authentication
- Responsive design

---

**Last Updated**: May 2026
**Maintained By**: CareerHub Development Team

Thank you for using CareerHub! Good luck with your career journey! 🚀
#   S t u d e n t - C a r e e r - P l a c e m e n t - P o r t a l - W e b s i t e 
 
 #   S t u d e n t - C a r e e r - P l a c e m e n t - P o r t a l - W e b s i t e 
 
 "# Student-Career-Placement-Portal-Website" 
