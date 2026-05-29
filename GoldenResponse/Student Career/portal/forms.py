"""
Forms for the Career Portal application with validation and security.
"""
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError
from django.utils.html import escape
import bleach
import re

from .models import Student, Skill, Project, PlacementTracker, ContactForm, InterviewNotes


class StudentRegistrationForm(UserCreationForm):
    """Secure student registration form with input validation."""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First name'
        })
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last name'
        })
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2')

    def clean_email(self):
        """Validate email uniqueness and format."""
        email = self.cleaned_data.get('email').lower().strip()
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        return email

    def clean_username(self):
        """Sanitize and validate username."""
        username = self.cleaned_data.get('username').strip()
        if not re.match(r'^[a-zA-Z0-9_-]+$', username):
            raise ValidationError("Username can only contain letters, numbers, underscores, and hyphens.")
        return username

    def clean_password1(self):
        """Validate password strength."""
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not any(c.isupper() for c in password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not any(c.isdigit() for c in password):
            raise ValidationError("Password must contain at least one digit.")
        return password


class StudentLoginForm(forms.Form):
    """Student login form with security features."""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter email'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )


class StudentProfileForm(forms.ModelForm):
    """Form for updating student profile information."""
    full_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    college = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    department = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    cgpa = forms.DecimalField(
        max_digits=3,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        required=False
    )
    profile_picture = forms.ImageField(required=False)
    resume = forms.FileField(required=False)

    class Meta:
        model = Student
        fields = ['full_name', 'college', 'department', 'semester', 'phone', 'cgpa', 'bio', 'profile_picture', 'resume']
        widgets = {
            'semester': forms.Select(attrs={'class': 'form-control'}),
        }

    def clean_phone(self):
        """Validate phone number format."""
        phone = self.cleaned_data.get('phone', '').strip()
        if phone and not re.match(r'^[0-9\s\-\+\(\)]{10,15}$', phone):
            raise ValidationError("Invalid phone number format.")
        return phone

    def clean_cgpa(self):
        """Validate CGPA range."""
        cgpa = self.cleaned_data.get('cgpa')
        if cgpa and (cgpa < 0 or cgpa > 10):
            raise ValidationError("CGPA must be between 0 and 10.")
        return cgpa

    def clean_full_name(self):
        """Sanitize full name."""
        full_name = self.cleaned_data.get('full_name', '').strip()
        # Remove potentially harmful characters
        full_name = bleach.clean(full_name, strip=True, allowed_tags=[])
        if not full_name:
            raise ValidationError("Full name is required.")
        return full_name


class SkillForm(forms.ModelForm):
    """Form for adding and updating student skills."""
    skill_name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Python, JavaScript'
        })
    )
    proficiency_level = forms.ChoiceField(
        choices=[(choice[0], choice[0]) for choice in [
            ('Beginner', 'Beginner'),
            ('Intermediate', 'Intermediate'),
            ('Advanced', 'Advanced'),
            ('Expert', 'Expert')
        ]],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    years_of_experience = forms.IntegerField(
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Skill
        fields = ['skill_name', 'proficiency_level', 'years_of_experience']

    def clean_skill_name(self):
        """Sanitize skill name."""
        skill_name = self.cleaned_data.get('skill_name', '').strip()
        skill_name = bleach.clean(skill_name, strip=True, allowed_tags=[])
        if not skill_name:
            raise ValidationError("Skill name is required.")
        return skill_name


class ProjectForm(forms.ModelForm):
    """Form for adding and updating student projects."""
    project_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Project name'
        })
    )
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Project description'
        })
    )
    technology_used = forms.CharField(
        max_length=500,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Python, Django, React (comma-separated)'
        })
    )
    github_link = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'GitHub repository link'
        })
    )
    live_link = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Live project link'
        })
    )
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )

    class Meta:
        model = Project
        fields = ['project_name', 'description', 'technology_used', 'github_link', 
                  'live_link', 'start_date', 'end_date', 'project_image', 'is_completed']
        widgets = {
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'project_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def clean_project_name(self):
        """Sanitize project name."""
        project_name = self.cleaned_data.get('project_name', '').strip()
        project_name = bleach.clean(project_name, strip=True, allowed_tags=[])
        if not project_name:
            raise ValidationError("Project name is required.")
        return project_name

    def clean_description(self):
        """Sanitize description."""
        description = self.cleaned_data.get('description', '').strip()
        description = bleach.clean(description, strip=True, allowed_tags=[])
        if not description:
            raise ValidationError("Description is required.")
        return description


class PlacementTrackerForm(forms.ModelForm):
    """Form for tracking placement preparation topics."""
    topic_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Topic name'
        })
    )
    category = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    status = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    completion_percentage = forms.IntegerField(
        min_value=0,
        max_value=100,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Completion %'
        })
    )
    notes = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Add notes'
        }),
        required=False
    )

    class Meta:
        model = PlacementTracker
        fields = ['category', 'topic_name', 'status', 'completion_percentage', 'notes', 'resources_link']
        widgets = {
            'resources_link': forms.URLInput(attrs={
                'class': 'form-control',
                'placeholder': 'Link to learning resource'
            })
        }

    def clean_topic_name(self):
        """Sanitize topic name."""
        topic_name = self.cleaned_data.get('topic_name', '').strip()
        topic_name = bleach.clean(topic_name, strip=True, allowed_tags=[])
        if not topic_name:
            raise ValidationError("Topic name is required.")
        return topic_name


class InterviewNotesForm(forms.ModelForm):
    """Form for saving interview preparation notes."""
    my_answer = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 6,
            'placeholder': 'Enter your answer here'
        })
    )
    custom_question = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Your custom question (if not selecting from library)'
        }),
        required=False
    )
    review_status = forms.ChoiceField(
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = InterviewNotes
        fields = ['my_answer', 'custom_question', 'review_status']

    def clean_my_answer(self):
        """Sanitize answer."""
        my_answer = self.cleaned_data.get('my_answer', '').strip()
        my_answer = bleach.clean(my_answer, strip=True, allowed_tags=['b', 'i', 'p', 'br'])
        if not my_answer:
            raise ValidationError("Answer is required.")
        return my_answer


class ContactFormForm(forms.ModelForm):
    """Form for contact/feedback submission with security."""
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your email'
        })
    )
    phone = forms.CharField(
        max_length=15,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your phone (optional)'
        })
    )
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject'
        })
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Your message'
        })
    )

    class Meta:
        model = ContactForm
        fields = ['name', 'email', 'phone', 'subject', 'message']

    def clean_name(self):
        """Sanitize name to prevent XSS."""
        name = self.cleaned_data.get('name', '').strip()
        name = bleach.clean(name, strip=True, allowed_tags=[])
        if not name:
            raise ValidationError("Name is required.")
        return name

    def clean_email(self):
        """Validate email format."""
        email = self.cleaned_data.get('email').lower().strip()
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError("Invalid email format.")
        return email

    def clean_message(self):
        """Sanitize message to prevent XSS."""
        message = self.cleaned_data.get('message', '').strip()
        message = bleach.clean(message, strip=True, allowed_tags=['b', 'i', 'p', 'br'])
        if not message:
            raise ValidationError("Message is required.")
        return message
