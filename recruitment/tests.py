from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserProfile, Skill, Candidate, JobListing, Application


class UserProfileTests(TestCase):
    def test_userprofile_role_saves(self):
        user = User.objects.create_user(username='test', password='pass')
        profile = UserProfile.objects.create(user=user, role='recruiter')
        self.assertEqual(profile.role, 'recruiter')

    def test_skill_name_saves(self):
        skill = Skill.objects.create(name='Customer Service',
            category='customer_service')
        self.assertEqual(skill.name, 'Customer Service')

    def test_candidate_name_saves(self):
        user = User.objects.create_user(username='cand', password='pass')
        candidate = Candidate.objects.create(user=user, first_name='John',
            last_name='Doe', cv_summary='Test CV')
        self.assertEqual(candidate.first_name, 'John')

    def test_joblisting_status_default(self):
        user = User.objects.create_user(username='rec', password='pass')
        job = JobListing.objects.create(title='Job', venue_name='Venue',
            venue_type='holiday_park', description='Test',
            employment_type='full_time', salary=20000, created_by=user)
        self.assertEqual(job.status, 'open')

    def test_application_status_default(self):
        user = User.objects.create_user(username='c1', password='pass')
        rec = User.objects.create_user(username='r1', password='pass')
        cand = Candidate.objects.create(user=user, first_name='Jane',
            last_name='Smith', cv_summary='CV')
        job = JobListing.objects.create(title='Job', venue_name='Venue',
            venue_type='theme_park', description='Test',
            employment_type='seasonal', salary=25000, created_by=rec)
        app = Application.objects.create(candidate=cand, job=job,
            cover_letter='Letter')
        self.assertEqual(app.status, 'pending')


class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_home_page_status_200(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_jobs_list_status_200(self):
        response = self.client.get('/jobs/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_status_200(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_register_page_status_200(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_dashboard_redirects_when_logged_out(self):
        response = self.client.get('/dashboard/')
        self.assertEqual(response.status_code, 302)

    def test_candidate_blocked_from_job_create(self):
        user = User.objects.create_user(username='test', password='pass')
        UserProfile.objects.create(user=user, role='candidate')
        self.client.login(username='test', password='pass')
        response = self.client.get('/jobs/create/')
        self.assertEqual(response.status_code, 403)

    def test_recruiter_blocked_from_candidate_create(self):
        user = User.objects.create_user(username='test', password='pass')
        UserProfile.objects.create(user=user, role='recruiter')
        self.client.login(username='test', password='pass')
        response = self.client.get('/candidates/create/')
        self.assertEqual(response.status_code, 403)

    def test_candidate_can_submit_application(self):
        user = User.objects.create_user(username='test', password='pass')
        rec = User.objects.create_user(username='rec', password='pass')
        UserProfile.objects.create(user=user, role='candidate')
        Candidate.objects.create(user=user, first_name='Test',
            last_name='User', cv_summary='CV')
        job = JobListing.objects.create(title='Test', venue_name='Venue',
            venue_type='resort', description='Test',
            employment_type='part_time', salary=22000, created_by=rec)

        self.client.login(username='test', password='pass')
        response = self.client.post(f'/apply/{job.id}/',
            {'cover_letter': 'My letter'})
        self.assertEqual(Application.objects.count(), 1)

    def test_duplicate_application_blocked(self):
        user = User.objects.create_user(username='test', password='pass')
        rec = User.objects.create_user(username='rec', password='pass')
        UserProfile.objects.create(user=user, role='candidate')
        cand = Candidate.objects.create(user=user, first_name='Test',
            last_name='User', cv_summary='CV')
        job = JobListing.objects.create(title='Test', venue_name='Venue',
            venue_type='adventure_park', description='Test',
            employment_type='full_time', salary=30000, created_by=rec)
        Application.objects.create(candidate=cand, job=job,
            cover_letter='Letter')

        self.client.login(username='test', password='pass')
        response = self.client.post(f'/apply/{job.id}/',
            {'cover_letter': 'Another letter'})
        self.assertEqual(Application.objects.count(), 1)

    def test_recruiter_can_update_app_status(self):
        user = User.objects.create_user(username='test', password='pass')
        rec = User.objects.create_user(username='rec', password='pass')
        UserProfile.objects.create(user=user, role='candidate')
        UserProfile.objects.create(user=rec, role='recruiter')
        cand = Candidate.objects.create(user=user, first_name='Test',
            last_name='User', cv_summary='CV')
        job = JobListing.objects.create(title='Test', venue_name='Venue',
            venue_type='holiday_park', description='Test',
            employment_type='seasonal', salary=28000, created_by=rec)
        app = Application.objects.create(candidate=cand, job=job,
            cover_letter='Letter')

        self.client.login(username='rec', password='pass')
        response = self.client.post(f'/applications/{app.id}/update/',
            {'status': 'shortlisted'})
        app.refresh_from_db()
        self.assertEqual(app.status, 'shortlisted')
