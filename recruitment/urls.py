from django.urls import path
from . import views
from . import job_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/recruiter/', views.dashboard_recruiter,
         name='dashboard_recruiter'),
    path('dashboard/candidate/', views.dashboard_candidate,
         name='dashboard_candidate'),
    path('dashboard/manager/', views.dashboard_manager,
         name='dashboard_manager'),
    path('candidates/', views.candidates_list, name='candidates_list'),
    path('candidates/create/', views.candidate_create, name='candidate_create'),
    path('candidates/<int:pk>/', views.candidate_detail, name='candidate_detail'),
    path('candidates/<int:pk>/edit/', views.candidate_edit, name='candidate_edit'),
    path('skills/', views.skills_manage, name='skills_manage'),
    path('jobs/', job_views.jobs_list, name='jobs_list'),
    path('jobs/create/', job_views.job_create, name='job_create'),
    path('jobs/<int:pk>/', job_views.job_detail, name='job_detail'),
    path('jobs/<int:pk>/edit/', job_views.job_edit, name='job_edit'),
    path('apply/<int:pk>/', job_views.apply_job, name='apply_job'),
    path('applications/', job_views.my_applications, name='my_applications'),
    path('applications/<int:pk>/', job_views.application_detail,
         name='application_detail'),
    path('applications/<int:pk>/update/', job_views.application_update,
         name='application_update'),
]
