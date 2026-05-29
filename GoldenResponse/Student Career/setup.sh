#!/bin/bash
# Setup script for Student Career & Placement Portal

echo "=========================================="
echo "Student Career Portal - Setup Script"
echo "=========================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 is installed"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please update .env file with your settings"
fi

# Run migrations
echo ""
echo "Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser
echo ""
echo "Creating superuser account..."
python manage.py createsuperuser

# Collect static files
echo ""
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Create necessary directories
echo ""
echo "Creating necessary directories..."
mkdir -p media/profiles media/resumes media/projects media/companies
mkdir -p staticfiles

echo ""
echo "=========================================="
echo "✓ Setup completed successfully!"
echo "=========================================="
echo ""
echo "To start the development server, run:"
echo "  source venv/bin/activate"
echo "  python manage.py runserver"
echo ""
echo "Then visit http://127.0.0.1:8000 in your browser"
echo ""
