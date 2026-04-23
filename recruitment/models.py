from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('recruiter', 'Recruiter'),
        ('candidate', 'Candidate'),
        ('manager', 'Manager'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ('technical', 'Technical'),
        ('physical', 'Physical'),
        ('customer_service', 'Customer Service'),
        ('safety', 'Safety'),
    ]
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name


class Candidate(models.Model):
    AVAILABILITY_CHOICES = [
        ('immediate', 'Immediate'),
        ('two_weeks', 'Two Weeks'),
        ('one_month', 'One Month'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    experience_years = models.IntegerField(default=0)
    cv_summary = models.TextField()
    availability = models.CharField(
        max_length=20, choices=AVAILABILITY_CHOICES)
    skills = models.ManyToManyField(Skill, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class JobListing(models.Model):
    VENUE_CHOICES = [
        ('holiday_park', 'Holiday Park'),
        ('theme_park', 'Theme Park'),
        ('resort', 'Resort'),
        ('adventure_park', 'Adventure Park'),
    ]
    TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
        ('seasonal', 'Seasonal'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('closed', 'Closed'),
    ]
    title = models.CharField(max_length=200)
    venue_name = models.CharField(max_length=200)
    venue_type = models.CharField(max_length=50, choices=VENUE_CHOICES)
    description = models.TextField()
    employment_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    salary = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='open')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('shortlisted', 'Shortlisted'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
    ]
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    job = models.ForeignKey(JobListing, on_delete=models.CASCADE)
    cover_letter = models.TextField()
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('candidate', 'job')

    def __str__(self):
        return f"{self.candidate} - {self.job}"
