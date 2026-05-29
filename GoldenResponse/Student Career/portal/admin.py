"""
Admin configuration for the Career Portal application.
"""
from django.contrib import admin
from .models import (
    Student, Skill, Project, PlacementTracker, InterviewQuestion,
    InterviewNotes, Opportunity, StudentApplication, ContactForm, Resource
)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'user', 'college', 'cgpa', 'created_at')
    list_filter = ('college', 'department', 'semester')
    search_fields = ('full_name', 'user__email', 'roll_number')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('skill_name', 'student', 'proficiency_level', 'endorsements')
    list_filter = ('proficiency_level', 'added_on')
    search_fields = ('skill_name', 'student__full_name')


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_name', 'student', 'is_completed', 'created_at')
    list_filter = ('is_completed', 'created_at')
    search_fields = ('project_name', 'student__full_name')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(PlacementTracker)
class PlacementTrackerAdmin(admin.ModelAdmin):
    list_display = ('topic_name', 'student', 'category', 'status', 'completion_percentage')
    list_filter = ('category', 'status', 'started_on')
    search_fields = ('topic_name', 'student__full_name')


@admin.register(InterviewQuestion)
class InterviewQuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'difficulty', 'company')
    list_filter = ('category', 'difficulty', 'company')
    search_fields = ('question', 'answer', 'company')


@admin.register(InterviewNotes)
class InterviewNotesAdmin(admin.ModelAdmin):
    list_display = ('student', 'review_status', 'created_at')
    list_filter = ('review_status', 'created_at')
    search_fields = ('student__full_name', 'my_answer')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'opportunity_type', 'status', 'posted_date')
    list_filter = ('opportunity_type', 'status', 'posted_date')
    search_fields = ('title', 'company', 'description')


@admin.register(StudentApplication)
class StudentApplicationAdmin(admin.ModelAdmin):
    list_display = ('student', 'opportunity', 'status', 'applied_date')
    list_filter = ('status', 'applied_date')
    search_fields = ('student__full_name', 'opportunity__title')


@admin.register(ContactForm)
class ContactFormAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_resolved', 'created_at')
    list_filter = ('is_resolved', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'subject')
        }),
        ('Message', {
            'fields': ('message',)
        }),
        ('Response', {
            'fields': ('is_resolved', 'response')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'resource_type', 'category', 'created_at')
    list_filter = ('resource_type', 'category', 'created_at')
    search_fields = ('title', 'description')
