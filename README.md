# Student Career & Placement Portal Website

A comprehensive, production-ready full-stack web application for students to manage their academic progress, placement preparation, projects, and career opportunities.

## Features

### 🎓 Core Features
- **Student Registration & Authentication**: Secure login/registration with password validation
- **Student Dashboard**: Personalized dashboard with statistics and quick actions
- **Profile Management**: Update personal information, upload resume, add profile picture
- **Skills Tracking**: Add and manage technical skills with proficiency levels
- **Project Portfolio**: Upload and showcase projects with GitHub links
- **Placement Tracker**: Track placement preparation topics by category
- **Interview Preparation**: Access question library and save personal notes
- **Job & Internship Opportunities**: Browse and apply for opportunities
- **Contact System**: Submit feedback and questions
- **Learning Resources**: Access curated learning materials

### 🔒 Security Features
- Password hashing using Django's authentication system
- CSRF protection on all forms
- SQL injection prevention via Django ORM
- XSS prevention using bleach library
- Email validation and format checking
- Input sanitization for all user inputs
- Secure session handling
- User role-based access control

## Technology Stack

### Frontend
- **HTML5**: Semantic markup for structure
- **CSS3**: Responsive design with custom styling
- **Bootstrap 5**: Responsive grid and components
- **JavaScript**: Interactive features and form validation
- **Font Awesome**: Icon library
- **Chart.js**: Data visualization

### Backend
- **Python 3.8+**: Programming language
- **Django 4.2**: Web framework
- **SQLite**: Database (default, can be upgraded to PostgreSQL)

### Additional Libraries
- `bleach`: XSS prevention and HTML sanitization
- `python-decouple`: Environment variable management
- `Pillow`: Image processing for profile pictures and project images
- `email-validator`: Email format validation

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Git (optional)

### Step 1: Clone or Download the Project
```bash
cd "Student Career"
```

### Step 2: Create Virtual Environment

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables
Create a `.env` file in the root directory (optional for development):
```
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=*
```

### Step 5: Apply Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser (Admin Account)
```bash
python manage.py createsuperuser
```
Follow the prompts to create an admin account.

### Step 7: Collect Static Files
```bash
python manage.py collectstatic --noinput
```

### Step 8: Load Initial Data (Optional)
To load sample interview questions and resources:
```bash
python manage.py loaddata initial_data
```

### Step 9: Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

## Usage

### For Students

1. **Register**: Create an account on the registration page
2. **Login**: Access your personalized dashboard
3. **Manage Profile**: Update your information, upload resume, and add skills
4. **Add Projects**: Showcase your portfolio with project details
5. **Track Placement**: Monitor your preparation progress
6. **Prepare for Interviews**: Access questions and save your answers
7. **Apply for Opportunities**: Browse and apply for internships/jobs
8. **Track Applications**: View your application status
9. **Access Resources**: Find learning materials and tools

### For Administrators

1. Access admin panel: `http://127.0.0.1:8000/admin/`
2. Login with superuser credentials
3. Manage:
   - Students and their profiles
   - Interview questions database
   - Job opportunities
   - Contact form submissions
   - Resources and links

## Project Structure

```
Student Career/
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
#   S t u d e n t - C a r e e r - P l a c e m e n t - P o r t a l - W e b s i t e  
 #   S t u d e n t - C a r e e r - P l a c e m e n t - P o r t a l - W e b s i t e  
 "# Student-Career-Placement-Portal-Website" 
