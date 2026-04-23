from django.contrib import admin
from .models import UserProfile, Skill, Candidate, JobListing, Application


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'role', 'phone']
    list_filter = ['role']
    search_fields = ['user__username', 'phone']


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ['name', 'category']
    list_filter = ['category']
    search_fields = ['name']


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'experience_years',
                    'availability']
    list_filter = ['availability']
    search_fields = ['first_name', 'last_name']


@admin.register(JobListing)
class JobListingAdmin(admin.ModelAdmin):
    list_display = ['title', 'venue_name', 'status', 'employment_type',
                    'created_at']
    list_filter = ['status', 'employment_type']
    search_fields = ['title', 'venue_name']


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['candidate', 'job', 'status', 'applied_at']
    list_filter = ['status']
    search_fields = ['candidate__first_name', 'job__title']
