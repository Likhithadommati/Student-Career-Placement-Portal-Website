"""
Views for the Career Portal application.
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse
from decimal import Decimal
import json

from .models import (
    Student, Skill, Project, PlacementTracker, InterviewQuestion,
    InterviewNotes, Opportunity, StudentApplication, ContactForm, Resource
)
from .forms import (
    StudentRegistrationForm, StudentLoginForm, StudentProfileForm,
    SkillForm, ProjectForm, PlacementTrackerForm, InterviewNotesForm,
    ContactFormForm
)


# ============= Authentication Views =============

def register(request):
    """Handle student registration with validation."""
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            # Create user
            user = form.save(commit=False)
            user.email = form.cleaned_data['email']
            user.save()
            
            # Create student profile
            Student.objects.create(
                user=user,
                full_name=f"{form.cleaned_data['first_name']} {form.cleaned_data['last_name']}"
            )
            
            messages.success(request, "Registration successful! Please log in.")
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = StudentRegistrationForm()
    
    return render(request, 'portal/register.html', {'form': form})


def login_view(request):
    """Handle student login."""
    if request.method == 'POST':
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            # Find user by email
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                
                if user is not None:
                    login(request, user)
                    messages.success(request, f"Welcome back, {user.first_name}!")
                    return redirect('dashboard')
                else:
                    messages.error(request, "Invalid password.")
            except User.DoesNotExist:
                messages.error(request, "Email not registered.")
    else:
        form = StudentLoginForm()
    
    return render(request, 'portal/login.html', {'form': form})


def logout_view(request):
    """Handle logout."""
    logout(request)
    messages.success(request, "Logged out successfully.")
    return redirect('home')


# ============= Landing Page Views =============

def home(request):
    """Render landing page with portal information."""
    # Get statistics
    total_students = Student.objects.count()
    total_opportunities = Opportunity.objects.filter(status='Active').count()
    resources = Resource.objects.all()[:6]  # Latest 6 resources
    interview_questions = InterviewQuestion.objects.all()[:5]
    
    context = {
        'total_students': total_students,
        'total_opportunities': total_opportunities,
        'resources': resources,
        'interview_questions': interview_questions,
    }
    return render(request, 'portal/index.html', context)


# ============= Dashboard Views =============

@login_required(login_url='login')
def dashboard(request):
    """Student dashboard with overview."""
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        # Create profile if it doesn't exist
        student = Student.objects.create(user=request.user, full_name=request.user.get_full_name())
    
    # Get student statistics
    skills_count = student.skills.count()
    projects_count = student.projects.count()
    placement_topics = student.placement_tracker.all()
    completed_topics = placement_topics.filter(status='Completed').count()
    recent_projects = student.projects.all()[:3]
    recent_applications = student.applications.all()[:3]
    
    context = {
        'student': student,
        'skills_count': skills_count,
        'projects_count': projects_count,
        'completed_topics': completed_topics,
        'total_topics': placement_topics.count(),
        'recent_projects': recent_projects,
        'recent_applications': recent_applications,
    }
    return render(request, 'portal/dashboard.html', context)


# ============= Profile Management =============

@login_required(login_url='login')
def profile(request):
    """View and edit student profile."""
    try:
        student = request.user.student_profile
    except Student.DoesNotExist:
        student = Student.objects.create(user=request.user, full_name=request.user.get_full_name())
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        form = StudentProfileForm(instance=student)
    
    context = {
        'form': form,
        'student': student,
    }
    return render(request, 'portal/profile.html', context)


# ============= Skills Management =============

@login_required(login_url='login')
def skills(request):
    """View and manage student skills."""
    student = request.user.student_profile
    skills_list = student.skills.all()
    
    context = {
        'skills': skills_list,
        'student': student,
    }
    return render(request, 'portal/skills.html', context)


@login_required(login_url='login')
def add_skill(request):
    """Add new skill."""
    student = request.user.student_profile
    
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.student = student
            skill.save()
            messages.success(request, "Skill added successfully!")
            return redirect('skills')
    else:
        form = SkillForm()
    
    context = {'form': form}
    return render(request, 'portal/add_skill.html', context)


@login_required(login_url='login')
def edit_skill(request, skill_id):
    """Edit existing skill."""
    student = request.user.student_profile
    skill = get_object_or_404(Skill, id=skill_id, student=student)
    
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, "Skill updated successfully!")
            return redirect('skills')
    else:
        form = SkillForm(instance=skill)
    
    context = {'form': form, 'skill': skill}
    return render(request, 'portal/add_skill.html', context)


@login_required(login_url='login')
def delete_skill(request, skill_id):
    """Delete skill."""
    student = request.user.student_profile
    skill = get_object_or_404(Skill, id=skill_id, student=student)
    skill.delete()
    messages.success(request, "Skill deleted successfully!")
    return redirect('skills')


# ============= Projects Management =============

@login_required(login_url='login')
def projects(request):
    """View and manage projects."""
    student = request.user.student_profile
    projects_list = student.projects.all()
    paginator = Paginator(projects_list, 6)
    page = request.GET.get('page')
    projects_page = paginator.get_page(page)
    
    context = {
        'projects': projects_page,
        'student': student,
    }
    return render(request, 'portal/projects.html', context)


@login_required(login_url='login')
def add_project(request):
    """Add new project."""
    student = request.user.student_profile
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.student = student
            project.save()
            messages.success(request, "Project added successfully!")
            return redirect('projects')
    else:
        form = ProjectForm()
    
    context = {'form': form}
    return render(request, 'portal/add_project.html', context)


@login_required(login_url='login')
def edit_project(request, project_id):
    """Edit existing project."""
    student = request.user.student_profile
    project = get_object_or_404(Project, id=project_id, student=student)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, "Project updated successfully!")
            return redirect('projects')
    else:
        form = ProjectForm(instance=project)
    
    context = {'form': form, 'project': project}
    return render(request, 'portal/add_project.html', context)


@login_required(login_url='login')
def delete_project(request, project_id):
    """Delete project."""
    student = request.user.student_profile
    project = get_object_or_404(Project, id=project_id, student=student)
    project.delete()
    messages.success(request, "Project deleted successfully!")
    return redirect('projects')


# ============= Placement Tracking =============

@login_required(login_url='login')
def placement_tracker(request):
    """View placement preparation tracking."""
    student = request.user.student_profile
    tracker = student.placement_tracker.all()
    
    # Group by category
    categories = {}
    for item in tracker:
        category = item.get_category_display()
        if category not in categories:
            categories[category] = []
        categories[category].append(item)
    
    context = {
        'tracker': tracker,
        'categories': categories,
        'student': student,
    }
    return render(request, 'portal/placement_tracker.html', context)


@login_required(login_url='login')
def add_placement_topic(request):
    """Add new placement preparation topic."""
    student = request.user.student_profile
    
    if request.method == 'POST':
        form = PlacementTrackerForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.student = student
            topic.save()
            messages.success(request, "Topic added to tracker!")
            return redirect('placement_tracker')
    else:
        form = PlacementTrackerForm()
    
    context = {'form': form}
    return render(request, 'portal/add_placement_topic.html', context)


@login_required(login_url='login')
def edit_placement_topic(request, topic_id):
    """Edit placement topic."""
    student = request.user.student_profile
    topic = get_object_or_404(PlacementTracker, id=topic_id, student=student)
    
    if request.method == 'POST':
        form = PlacementTrackerForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, "Topic updated!")
            return redirect('placement_tracker')
    else:
        form = PlacementTrackerForm(instance=topic)
    
    context = {'form': form, 'topic': topic}
    return render(request, 'portal/add_placement_topic.html', context)


@login_required(login_url='login')
def delete_placement_topic(request, topic_id):
    """Delete placement topic."""
    student = request.user.student_profile
    topic = get_object_or_404(PlacementTracker, id=topic_id, student=student)
    topic.delete()
    messages.success(request, "Topic deleted!")
    return redirect('placement_tracker')


# ============= Interview Preparation =============

@login_required(login_url='login')
def interview_prep(request):
    """Interview preparation with question library."""
    questions = InterviewQuestion.objects.all()
    category = request.GET.get('category')
    
    if category:
        questions = questions.filter(category=category)
    
    paginator = Paginator(questions, 5)
    page = request.GET.get('page')
    questions_page = paginator.get_page(page)
    
    categories = InterviewQuestion.objects.values('category').distinct()
    
    context = {
        'questions': questions_page,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'portal/interview_prep.html', context)


@login_required(login_url='login')
def interview_notes(request):
    """View interview notes."""
    student = request.user.student_profile
    notes = student.interview_notes.all()
    
    context = {
        'notes': notes,
        'student': student,
    }
    return render(request, 'portal/interview_notes.html', context)


@login_required(login_url='login')
def add_interview_note(request, question_id=None):
    """Add interview note."""
    student = request.user.student_profile
    question = None
    
    if question_id:
        question = get_object_or_404(InterviewQuestion, id=question_id)
    
    if request.method == 'POST':
        form = InterviewNotesForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.student = student
            if question:
                note.question = question
            note.save()
            messages.success(request, "Note saved!")
            return redirect('interview_notes')
    else:
        form = InterviewNotesForm()
    
    context = {
        'form': form,
        'question': question,
    }
    return render(request, 'portal/add_interview_note.html', context)


@login_required(login_url='login')
def edit_interview_note(request, note_id):
    """Edit interview note."""
    student = request.user.student_profile
    note = get_object_or_404(InterviewNotes, id=note_id, student=student)
    
    if request.method == 'POST':
        form = InterviewNotesForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated!")
            return redirect('interview_notes')
    else:
        form = InterviewNotesForm(instance=note)
    
    context = {'form': form, 'note': note}
    return render(request, 'portal/add_interview_note.html', context)


@login_required(login_url='login')
def delete_interview_note(request, note_id):
    """Delete interview note."""
    student = request.user.student_profile
    note = get_object_or_404(InterviewNotes, id=note_id, student=student)
    note.delete()
    messages.success(request, "Note deleted!")
    return redirect('interview_notes')


# ============= Internships & Jobs =============

@login_required(login_url='login')
def opportunities(request):
    """View internship and job opportunities."""
    opps = Opportunity.objects.filter(status='Active')
    opp_type = request.GET.get('type')
    search = request.GET.get('search')
    
    if opp_type:
        opps = opps.filter(opportunity_type=opp_type)
    
    if search:
        opps = opps.filter(
            Q(title__icontains=search) |
            Q(company__icontains=search) |
            Q(description__icontains=search)
        )
    
    paginator = Paginator(opps, 6)
    page = request.GET.get('page')
    opportunities_page = paginator.get_page(page)
    
    context = {
        'opportunities': opportunities_page,
        'selected_type': opp_type,
        'search_query': search,
    }
    return render(request, 'portal/opportunities.html', context)


@login_required(login_url='login')
def opportunity_detail(request, opportunity_id):
    """View opportunity details."""
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    student = request.user.student_profile
    
    # Check if already applied
    already_applied = StudentApplication.objects.filter(
        student=student,
        opportunity=opportunity
    ).exists()
    
    context = {
        'opportunity': opportunity,
        'already_applied': already_applied,
    }
    return render(request, 'portal/opportunity_detail.html', context)


@login_required(login_url='login')
def apply_opportunity(request, opportunity_id):
    """Apply for opportunity."""
    student = request.user.student_profile
    opportunity = get_object_or_404(Opportunity, id=opportunity_id)
    
    # Check if already applied
    application, created = StudentApplication.objects.get_or_create(
        student=student,
        opportunity=opportunity,
        defaults={'status': 'Applied'}
    )
    
    if created:
        messages.success(request, "Application submitted!")
    else:
        messages.info(request, "You have already applied for this opportunity.")
    
    return redirect('opportunity_detail', opportunity_id=opportunity_id)


@login_required(login_url='login')
def my_applications(request):
    """View student's applications."""
    student = request.user.student_profile
    applications = student.applications.all()
    
    context = {
        'applications': applications,
        'student': student,
    }
    return render(request, 'portal/my_applications.html', context)


# ============= Contact Form =============

def contact(request):
    """Handle contact form submission."""
    if request.method == 'POST':
        form = ContactFormForm(request.POST)
        if form.is_valid():
            contact = form.save()
            messages.success(request, "Thank you! We'll get back to you soon.")
            return redirect('home')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        form = ContactFormForm()
    
    context = {'form': form}
    return render(request, 'portal/contact.html', context)


# ============= Resources =============

def resources(request):
    """View learning resources."""
    resources_list = Resource.objects.all()
    category = request.GET.get('category')
    resource_type = request.GET.get('type')
    
    if category:
        resources_list = resources_list.filter(category__icontains=category)
    
    if resource_type:
        resources_list = resources_list.filter(resource_type=resource_type)
    
    paginator = Paginator(resources_list, 9)
    page = request.GET.get('page')
    resources_page = paginator.get_page(page)
    
    context = {
        'resources': resources_page,
        'selected_category': category,
        'selected_type': resource_type,
    }
    return render(request, 'portal/resources.html', context)


# ============= Error Handlers =============

def custom_404(request, exception):
    """Handle 404 errors."""
    return render(request, 'portal/404.html', status=404)


def custom_500(request):
    """Handle 500 errors."""
    return render(request, 'portal/500.html', status=500)
