from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recruitment.models import UserProfile, Skill, Candidate, JobListing, Application


class Command(BaseCommand):
    help = 'Seed database with test data'

    def handle(self, *args, **options):
        # Create users
        admin = User.objects.create_superuser('admin', 'admin@admin.com',
            'password')
        self.stdout.write('[OK] Created admin user')

        manager = User.objects.create_user(username='manager1',
            email='manager1@primerecruit.com', password='password')
        UserProfile.objects.create(user=manager, role='manager')
        self.stdout.write('[OK] Created manager1 user')

        rec1 = User.objects.create_user(username='recruiter1',
            email='recruiter1@primerecruit.com', password='password')
        UserProfile.objects.create(user=rec1, role='recruiter')
        self.stdout.write('[OK] Created recruiter1 user')

        rec2 = User.objects.create_user(username='recruiter2',
            email='recruiter2@primerecruit.com', password='password')
        UserProfile.objects.create(user=rec2, role='recruiter')
        self.stdout.write('[OK] Created recruiter2 user')

        cand1_user = User.objects.create_user(username='candidate1',
            email='candidate1@primerecruit.com', password='password')
        UserProfile.objects.create(user=cand1_user, role='candidate')
        self.stdout.write('[OK] Created candidate1 user')

        cand2_user = User.objects.create_user(username='candidate2',
            email='candidate2@primerecruit.com', password='password')
        UserProfile.objects.create(user=cand2_user, role='candidate')
        self.stdout.write('[OK] Created candidate2 user')

        cand3_user = User.objects.create_user(username='candidate3',
            email='candidate3@primerecruit.com', password='password')
        UserProfile.objects.create(user=cand3_user, role='candidate')
        self.stdout.write('[OK] Created candidate3 user')

        # Create skills
        cs = Skill.objects.create(name='Customer Service',
            category='customer_service')
        fa = Skill.objects.create(name='First Aid', category='safety')
        lg = Skill.objects.create(name='Lifeguarding', category='safety')
        ro = Skill.objects.create(name='Ride Operations', category='technical')
        tl = Skill.objects.create(name='Team Leadership',
            category='technical')
        ch = Skill.objects.create(name='Cash Handling',
            category='customer_service')
        fh = Skill.objects.create(name='Food Hygiene', category='safety')
        cm = Skill.objects.create(name='Crowd Management', category='physical')
        self.stdout.write('[OK] Created 8 skills')

        # Create candidates
        cand1 = Candidate.objects.create(user=cand1_user, first_name='John',
            last_name='Smith', experience_years=2, cv_summary='Experienced',
            availability='immediate')
        cand1.skills.add(cs, lg)
        self.stdout.write('[OK] Created John Smith candidate with skills')

        cand2 = Candidate.objects.create(user=cand2_user, first_name='Sarah',
            last_name='Jones', experience_years=3, cv_summary='Skilled',
            availability='two_weeks')
        cand2.skills.add(tl, fa)
        self.stdout.write('[OK] Created Sarah Jones candidate with skills')

        cand3 = Candidate.objects.create(user=cand3_user, first_name='Mike',
            last_name='Brown', experience_years=1, cv_summary='Enthusiastic',
            availability='one_month')
        cand3.skills.add(ch, fh)
        self.stdout.write('[OK] Created Mike Brown candidate with skills')

        # Create jobs
        job1 = JobListing.objects.create(title='Lifeguard',
            venue_name='Sunburst Holiday Park', venue_type='holiday_park',
            description='Qualified lifeguard needed at Sunburst Holiday Park',
            employment_type='seasonal', salary=28000, created_by=rec1)

        job2 = JobListing.objects.create(title='Ride Operator',
            venue_name='Galactic Theme Park', venue_type='theme_park',
            description='Ride operators for exciting attractions in Cork',
            employment_type='full_time', salary=25000, created_by=rec1)

        job3 = JobListing.objects.create(title='Customer Host',
            venue_name='Azure Beach Resort', venue_type='resort',
            description='Friendly hosts at Azure Beach Resort in Galway',
            employment_type='part_time', salary=22000, created_by=rec1)

        job4 = JobListing.objects.create(title='Activity Leader',
            venue_name='WildRush Adventure Park', venue_type='adventure_park',
            description='Leaders for outdoor activity programmes in Limerick',
            employment_type='full_time', salary=30000, created_by=rec1)
        self.stdout.write('[OK] Created 4 job listings')

        # Create applications
        Application.objects.create(candidate=cand1, job=job1,
            cover_letter='I am a qualified lifeguard', status='pending')
        self.stdout.write('[OK] John Smith applied to Lifeguard (pending)')

        Application.objects.create(candidate=cand2, job=job1,
            cover_letter='I have first aid training', status='shortlisted')
        self.stdout.write('[OK] Sarah Jones applied to Lifeguard (shortlisted)')

        Application.objects.create(candidate=cand3, job=job2,
            cover_letter='Excited to operate rides', status='pending')
        self.stdout.write('[OK] Mike Brown applied to Ride Operator (pending)')

        self.stdout.write(self.style.SUCCESS('Seed data complete!'))
