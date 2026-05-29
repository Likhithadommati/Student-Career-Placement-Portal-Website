"""
Database models for the Career Portal application.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.utils import timezone


class Student(models.Model):
    """Student profile model with career-related information."""
    SEMESTER_CHOICES = [
        ('1', '1st Semester'),
        ('2', '2nd Semester'),
        ('3', '3rd Semester'),
        ('4', '4th Semester'),
        ('5', '5th Semester'),
        ('6', '6th Semester'),
        ('7', '7th Semester'),
        ('8', '8th Semester'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    full_name = models.CharField(max_length=100, blank=True)
    college = models.CharField(max_length=150, blank=True)
    department = models.CharField(max_length=100, blank=True)
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES, default='1')
    phone = models.CharField(max_length=15, blank=True)
    roll_number = models.CharField(max_length=50, unique=True, blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    bio = models.TextField(blank=True)
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.user.email}"

    class Meta:
        ordering = ['-created_at']


class Skill(models.Model):
    """Student skills tracking model."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=100)
    proficiency_level = models.CharField(
        max_length=20,
        choices=[('Beginner', 'Beginner'), ('Intermediate', 'Intermediate'), ('Advanced', 'Advanced'), ('Expert', 'Expert')],
        default='Beginner'
    )
    years_of_experience = models.IntegerField(default=0)
    endorsements = models.IntegerField(default=0)
    added_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.skill_name}"

    class Meta:
        unique_together = ('student', 'skill_name')
        ordering = ['-endorsements', '-added_on']


class Project(models.Model):
    """Student project portfolio model."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='projects')
    project_name = models.CharField(max_length=200)
    description = models.TextField()
    technology_used = models.CharField(max_length=500)  # Comma-separated or JSON format
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    project_image = models.ImageField(upload_to='projects/', null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project_name} - {self.student.full_name}"

    class Meta:
        ordering = ['-created_at']


class PlacementTracker(models.Model):
    """Placement preparation tracking model."""
    TOPIC_STATUS = [
        ('Not Started', 'Not Started'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Reviewed', 'Reviewed'),
    ]

    CATEGORY_CHOICES = [
        ('DSA', 'Data Structures & Algorithms'),
        ('WEB', 'Web Development'),
        ('ML', 'Machine Learning'),
        ('DATABASE', 'Database Management'),
        ('OS', 'Operating Systems'),
        ('NETWORKING', 'Networking'),
        ('SYSTEM_DESIGN', 'System Design'),
        ('BEHAVIORAL', 'Behavioral Interview'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='placement_tracker')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    topic_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=TOPIC_STATUS, default='Not Started')
    completion_percentage = models.IntegerField(default=0)
    started_on = models.DateTimeField(auto_now_add=True)
    completed_on = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    resources_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.topic_name}"

    class Meta:
        ordering = ['-started_on']


class InterviewQuestion(models.Model):
    """Interview preparation - frequently asked questions."""
    category = models.CharField(
        max_length=50,
        choices=[
            ('DSA', 'Data Structures'),
            ('WEB', 'Web Development'),
            ('DATABASE', 'Database'),
            ('SYSTEM', 'System Design'),
            ('BEHAVIORAL', 'Behavioral'),
        ]
    )
    question = models.TextField()
    answer = models.TextField()
    difficulty = models.CharField(
        max_length=10,
        choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')],
        default='Medium'
    )
    company = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - {self.question[:50]}"

    class Meta:
        ordering = ['difficulty', '-created_at']


class InterviewNotes(models.Model):
    """Student's personal interview notes."""
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='interview_notes')
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE, blank=True, null=True)
    custom_question = models.TextField(blank=True)
    my_answer = models.TextField()
    review_status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Good', 'Good'), ('Needs Work', 'Needs Work'), ('Excellent', 'Excellent')],
        default='Pending'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Notes by {self.student.full_name}"

    class Meta:
        ordering = ['-created_at']


class Opportunity(models.Model):
    """Internship and Job opportunities listing."""
    OPPORTUNITY_TYPE = [
        ('Internship', 'Internship'),
        ('Full-time', 'Full-time Job'),
        ('Part-time', 'Part-time Job'),
    ]

    STATUS_CHOICES = [
        ('Active', 'Active'),
        ('Closed', 'Closed'),
        ('On Hold', 'On Hold'),
    ]

    title = models.CharField(max_length=200)
    company = models.CharField(max_length=150)
    description = models.TextField()
    opportunity_type = models.CharField(max_length=20, choices=OPPORTUNITY_TYPE)
    location = models.CharField(max_length=100, blank=True)
    salary_range = models.CharField(max_length=50, blank=True)
    required_skills = models.CharField(max_length=500)
    job_link = models.URLField()
    posted_date = models.DateTimeField(auto_now_add=True)
    last_date_to_apply = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    company_logo = models.ImageField(upload_to='companies/', null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.company}"

    class Meta:
        ordering = ['-posted_date']


class StudentApplication(models.Model):
    """Track student applications for opportunities."""
    APPLICATION_STATUS = [
        ('Applied', 'Applied'),
        ('Shortlisted', 'Shortlisted'),
        ('Interview', 'Interview Scheduled'),
        ('Offered', 'Offered'),
        ('Rejected', 'Rejected'),
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='applications')
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE, related_name='applications')
    status = models.CharField(max_length=20, choices=APPLICATION_STATUS, default='Applied')
    applied_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.opportunity.title}"

    class Meta:
        unique_together = ('student', 'opportunity')
        ordering = ['-applied_date']


class ContactForm(models.Model):
    """Contact form submissions."""
    name = models.CharField(max_length=100)
    email = models.EmailField(validators=[EmailValidator()])
    subject = models.CharField(max_length=200)
    message = models.TextField()
    phone = models.CharField(max_length=15, blank=True)
    is_resolved = models.BooleanField(default=False)
    response = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-created_at']


class Resource(models.Model):
    """Career resources and learning materials."""
    RESOURCE_TYPE = [
        ('Article', 'Article'),
        ('Video', 'Video'),
        ('Course', 'Course'),
        ('Blog', 'Blog Post'),
        ('Tool', 'Tool'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    resource_type = models.CharField(max_length=20, choices=RESOURCE_TYPE)
    url = models.URLField()
    category = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} - {self.resource_type}"

    class Meta:
        ordering = ['-created_at']
