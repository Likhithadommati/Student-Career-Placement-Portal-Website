@echo off
REM Setup script for Student Career & Placement Portal (Windows)

echo.
echo ==========================================
echo Student Career Portal - Setup Script
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher from https://www.python.org/
    pause
    exit /b 1
)

echo OK: Python is installed
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo.
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Create .env file if it doesn't exist
if not exist .env (
    echo.
    echo Creating .env file from template...
    copy .env.example .env
    echo Warning: Please update .env file with your settings
)

REM Run migrations
echo.
echo Running database migrations...
python manage.py makemigrations
python manage.py migrate

REM Create superuser
echo.
echo Creating superuser account...
python manage.py createsuperuser

REM Collect static files
echo.
echo Collecting static files...
python manage.py collectstatic --noinput

REM Create necessary directories
echo.
echo Creating necessary directories...
if not exist media\profiles mkdir media\profiles
if not exist media\resumes mkdir media\resumes
if not exist media\projects mkdir media\projects
if not exist media\companies mkdir media\companies
if not exist staticfiles mkdir staticfiles

echo.
echo ==========================================
echo Setup completed successfully!
echo ==========================================
echo.
echo To start the development server, run:
echo   venv\Scripts\activate.bat
echo   python manage.py runserver
echo.
echo Then visit http://127.0.0.1:8000 in your browser
echo.
pause
