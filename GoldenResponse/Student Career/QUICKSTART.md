# INSTALLATION & QUICK START GUIDE

## Quick Setup (Windows)

### Step 1: Navigate to Project
```
cd "Student Career"
```

### Step 2: Run Setup Script
Double-click `setup.bat` and follow the prompts.

The script will automatically:
- Create virtual environment
- Install dependencies
- Set up database
- Create admin account
- Prepare static files

### Step 3: Start Server
After setup completes:
```
venv\Scripts\activate.bat
python manage.py runserver
```

### Step 4: Access Application
Open browser and go to: **http://127.0.0.1:8000**

---

## Quick Setup (macOS/Linux)

### Step 1: Navigate to Project
```bash
cd "Student Career"
```

### Step 2: Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Start Server
```bash
source venv/bin/activate
python manage.py runserver
```

### Step 4: Access Application
Open browser and go to: **http://127.0.0.1:8000**

---

## Manual Setup (If Automated Script Doesn't Work)

### Windows:
```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate.bat

# Install packages
pip install -r requirements.txt

# Setup database
python manage.py makemigrations
python manage.py migrate

# Create admin account
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run server
python manage.py runserver
```

### macOS/Linux:
```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Setup database
python manage.py makemigrations
python manage.py migrate

# Create admin account
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput

# Run server
python manage.py runserver
```

---

## First-Time Login

### Student Account:
1. Go to **http://127.0.0.1:8000/register/**
2. Create new account
3. Login with credentials

### Admin Panel:
1. Go to **http://127.0.0.1:8000/admin/**
2. Login with superuser account (created during setup)

---

## Adding Initial Data

### Via Admin Panel:
1. Login to admin at http://127.0.0.1:8000/admin/
2. Add Interview Questions
3. Add Opportunities (Jobs/Internships)
4. Add Resources

### Via Python Shell:
```python
python manage.py shell
>>> from portal.models import InterviewQuestion
>>> InterviewQuestion.objects.create(
...     category='DSA',
...     question='What is a binary search tree?',
...     answer='A BST is a tree where left child < parent < right child',
...     difficulty='Medium',
...     company='Google'
... )
```

---

## Key Features to Explore

1. **Landing Page**: http://127.0.0.1:8000/
2. **Register**: http://127.0.0.1:8000/register/
3. **Dashboard**: http://127.0.0.1:8000/dashboard/ (after login)
4. **Skills**: http://127.0.0.1:8000/skills/
5. **Projects**: http://127.0.0.1:8000/projects/
6. **Placement Tracker**: http://127.0.0.1:8000/placement-tracker/
7. **Interview Prep**: http://127.0.0.1:8000/interview-prep/
8. **Opportunities**: http://127.0.0.1:8000/opportunities/
9. **Contact**: http://127.0.0.1:8000/contact/
10. **Admin Panel**: http://127.0.0.1:8000/admin/

---

## File Structure

```
Student Career/
├── manage.py                      # Django management
├── requirements.txt               # Python dependencies
├── README.md                      # Main documentation
├── DEPLOYMENT.md                  # Production guide
├── setup.bat / setup.sh           # Setup scripts
├── .env.example                   # Environment template
│
├── career_portal/                 # Main Django project
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── portal/                        # Main app
│   ├── models.py                  # Database models
│   ├── views.py                   # View logic
│   ├── forms.py                   # Form validation
│   ├── urls.py                    # URL routing
│   ├── admin.py                   # Admin config
│   └── migrations/
│
├── templates/                     # HTML templates
│   ├── base.html
│   └── portal/
│       ├── index.html
│       ├── register.html
│       ├── dashboard.html
│       └── ... (other pages)
│
├── static/                        # CSS, JS, Images
│   ├── css/style.css
│   ├── js/main.js
│   └── images/
│
└── media/                         # User uploads
    ├── profiles/
    ├── resumes/
    ├── projects/
    └── companies/
```

---

## Troubleshooting

### Port 8000 Already in Use
```bash
python manage.py runserver 8001
```

### Database Error
```bash
# Reset database (development only)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Static Files Not Loading
```bash
python manage.py collectstatic --clear --noinput
```

### Virtual Environment Issues
```bash
# Delete and recreate
rm -rf venv
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate.bat
pip install -r requirements.txt
```

---

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate              # Linux/Mac
venv\Scripts\activate.bat             # Windows

# Run development server
python manage.py runserver

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Access Django shell
python manage.py shell

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Create admin user from shell
python manage.py shell
>>> from django.contrib.auth.models import User
>>> User.objects.create_superuser('admin', 'admin@example.com', 'password')

# Clear database and start fresh
python manage.py flush
```

---

## Next Steps

After installation:

1. **Customize Settings**: Edit `career_portal/settings.py` for your needs
2. **Add Initial Data**: Add interview questions and opportunities via admin
3. **Customize Branding**: Update company name, colors, logo
4. **Test All Features**: Register, login, add skills/projects
5. **Deploy**: Follow DEPLOYMENT.md for production setup

---

## Support

For issues or questions:
- Check README.md for detailed documentation
- Review Django documentation: https://docs.djangoproject.com/
- Check console for error messages
- Review logs in development

---

**Congratulations!** Your Student Career Portal is ready to use! 🎉

For production deployment, see DEPLOYMENT.md
