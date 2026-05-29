"""
URL configuration for the portal app.
"""
from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
    
    # Skills
    path('skills/', views.skills, name='skills'),
    path('skills/add/', views.add_skill, name='add_skill'),
    path('skills/edit/<int:skill_id>/', views.edit_skill, name='edit_skill'),
    path('skills/delete/<int:skill_id>/', views.delete_skill, name='delete_skill'),
    
    # Projects
    path('projects/', views.projects, name='projects'),
    path('projects/add/', views.add_project, name='add_project'),
    path('projects/edit/<int:project_id>/', views.edit_project, name='edit_project'),
    path('projects/delete/<int:project_id>/', views.delete_project, name='delete_project'),
    
    # Placement Tracking
    path('placement-tracker/', views.placement_tracker, name='placement_tracker'),
    path('placement-tracker/add/', views.add_placement_topic, name='add_placement_topic'),
    path('placement-tracker/edit/<int:topic_id>/', views.edit_placement_topic, name='edit_placement_topic'),
    path('placement-tracker/delete/<int:topic_id>/', views.delete_placement_topic, name='delete_placement_topic'),
    
    # Interview Preparation
    path('interview-prep/', views.interview_prep, name='interview_prep'),
    path('interview-notes/', views.interview_notes, name='interview_notes'),
    path('interview-notes/add/', views.add_interview_note, name='add_interview_note'),
    path('interview-notes/add/<int:question_id>/', views.add_interview_note, name='add_interview_note_with_question'),
    path('interview-notes/edit/<int:note_id>/', views.edit_interview_note, name='edit_interview_note'),
    path('interview-notes/delete/<int:note_id>/', views.delete_interview_note, name='delete_interview_note'),
    
    # Opportunities
    path('opportunities/', views.opportunities, name='opportunities'),
    path('opportunities/<int:opportunity_id>/', views.opportunity_detail, name='opportunity_detail'),
    path('opportunities/<int:opportunity_id>/apply/', views.apply_opportunity, name='apply_opportunity'),
    path('my-applications/', views.my_applications, name='my_applications'),
    
    # Resources
    path('resources/', views.resources, name='resources'),
    
    # Contact
    path('contact/', views.contact, name='contact'),
]
