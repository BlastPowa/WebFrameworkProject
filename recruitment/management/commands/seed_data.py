from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from recruitment.models import UserProfile, Skill, Candidate, JobListing, Application


class Command(BaseCommand):
    help = 'Seed database with test data'

    def handle(self, *args, **options):
        # Create users
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser('admin', 'admin@admin.com',
                'password')
            self.stdout.write('[OK] Created admin user')
        else:
            admin = User.objects.get(username='admin')
            self.stdout.write('[OK] Admin user already exists')

        if not User.objects.filter(username='manager1').exists():
            manager = User.objects.create_user(username='manager1',
                email='manager1@primerecruit.com', password='password')
            UserProfile.objects.create(user=manager, role='manager')
            self.stdout.write('[OK] Created manager1 user')
        else:
            manager = User.objects.get(username='manager1')
            self.stdout.write('[OK] manager1 user already exists')

        if not User.objects.filter(username='recruiter1').exists():
            rec1 = User.objects.create_user(username='recruiter1',
                email='recruiter1@primerecruit.com', password='password')
            UserProfile.objects.create(user=rec1, role='recruiter')
            self.stdout.write('[OK] Created recruiter1 user')
        else:
            rec1 = User.objects.get(username='recruiter1')
            self.stdout.write('[OK] recruiter1 user already exists')

        if not User.objects.filter(username='recruiter2').exists():
            rec2 = User.objects.create_user(username='recruiter2',
                email='recruiter2@primerecruit.com', password='password')
            UserProfile.objects.create(user=rec2, role='recruiter')
            self.stdout.write('[OK] Created recruiter2 user')
        else:
            rec2 = User.objects.get(username='recruiter2')
            self.stdout.write('[OK] recruiter2 user already exists')

        if not User.objects.filter(username='candidate1').exists():
            cand1_user = User.objects.create_user(username='candidate1',
                email='candidate1@primerecruit.com', password='password')
            UserProfile.objects.create(user=cand1_user, role='candidate')
            self.stdout.write('[OK] Created candidate1 user')
        else:
            cand1_user = User.objects.get(username='candidate1')
            self.stdout.write('[OK] candidate1 user already exists')

        if not User.objects.filter(username='candidate2').exists():
            cand2_user = User.objects.create_user(username='candidate2',
                email='candidate2@primerecruit.com', password='password')
            UserProfile.objects.create(user=cand2_user, role='candidate')
            self.stdout.write('[OK] Created candidate2 user')
        else:
            cand2_user = User.objects.get(username='candidate2')
            self.stdout.write('[OK] candidate2 user already exists')

        if not User.objects.filter(username='candidate3').exists():
            cand3_user = User.objects.create_user(username='candidate3',
                email='candidate3@primerecruit.com', password='password')
            UserProfile.objects.create(user=cand3_user, role='candidate')
            self.stdout.write('[OK] Created candidate3 user')
        else:
            cand3_user = User.objects.get(username='candidate3')
            self.stdout.write('[OK] candidate3 user already exists')

        # Create skills
        cs, _ = Skill.objects.get_or_create(name='Customer Service',
            defaults={'category': 'customer_service'})
        fa, _ = Skill.objects.get_or_create(name='First Aid',
            defaults={'category': 'safety'})
        lg, _ = Skill.objects.get_or_create(name='Lifeguarding',
            defaults={'category': 'safety'})
        ro, _ = Skill.objects.get_or_create(name='Ride Operations',
            defaults={'category': 'technical'})
        tl, _ = Skill.objects.get_or_create(name='Team Leadership',
            defaults={'category': 'technical'})
        ch, _ = Skill.objects.get_or_create(name='Cash Handling',
            defaults={'category': 'customer_service'})
        fh, _ = Skill.objects.get_or_create(name='Food Hygiene',
            defaults={'category': 'safety'})
        cm, _ = Skill.objects.get_or_create(name='Crowd Management',
            defaults={'category': 'physical'})
        self.stdout.write('[OK] Created or retrieved 8 skills')

        # Create candidates
        cand1, _ = Candidate.objects.get_or_create(user=cand1_user,
            defaults={'first_name': 'John', 'last_name': 'Smith',
            'experience_years': 2, 'cv_summary': 'Experienced',
            'availability': 'immediate'})
        if not cand1.skills.exists():
            cand1.skills.add(cs, lg)
        self.stdout.write('[OK] Created or retrieved John Smith candidate')

        cand2, _ = Candidate.objects.get_or_create(user=cand2_user,
            defaults={'first_name': 'Sarah', 'last_name': 'Jones',
            'experience_years': 3, 'cv_summary': 'Skilled',
            'availability': 'two_weeks'})
        if not cand2.skills.exists():
            cand2.skills.add(tl, fa)
        self.stdout.write('[OK] Created or retrieved Sarah Jones candidate')

        cand3, _ = Candidate.objects.get_or_create(user=cand3_user,
            defaults={'first_name': 'Mike', 'last_name': 'Brown',
            'experience_years': 1, 'cv_summary': 'Enthusiastic',
            'availability': 'one_month'})
        if not cand3.skills.exists():
            cand3.skills.add(ch, fh)
        self.stdout.write('[OK] Created or retrieved Mike Brown candidate')

        # Create jobs
        job1, _ = JobListing.objects.get_or_create(title='Lifeguard',
            defaults={'venue_name': 'Sunburst Holiday Park',
            'venue_type': 'holiday_park',
            'description': 'Qualified lifeguard needed at Sunburst Holiday Park',
            'employment_type': 'seasonal', 'salary': 28000, 'created_by': rec1})

        job2, _ = JobListing.objects.get_or_create(title='Ride Operator',
            defaults={'venue_name': 'Galactic Theme Park',
            'venue_type': 'theme_park',
            'description': 'Ride operators for exciting attractions in Cork',
            'employment_type': 'full_time', 'salary': 25000, 'created_by': rec1})

        job3, _ = JobListing.objects.get_or_create(title='Customer Host',
            defaults={'venue_name': 'Azure Beach Resort',
            'venue_type': 'resort',
            'description': 'Friendly hosts at Azure Beach Resort in Galway',
            'employment_type': 'part_time', 'salary': 22000, 'created_by': rec1})

        job4, _ = JobListing.objects.get_or_create(title='Activity Leader',
            defaults={'venue_name': 'WildRush Adventure Park',
            'venue_type': 'adventure_park',
            'description': 'Leaders for outdoor activity programmes in Limerick',
            'employment_type': 'full_time', 'salary': 30000, 'created_by': rec1})
        self.stdout.write('[OK] Created or retrieved 4 job listings')

        # Create applications
        Application.objects.get_or_create(candidate=cand1, job=job1,
            defaults={'cover_letter': 'I am a qualified lifeguard', 'status': 'pending'})
        self.stdout.write('[OK] John Smith applied to Lifeguard (pending)')

        Application.objects.get_or_create(candidate=cand2, job=job1,
            defaults={'cover_letter': 'I have first aid training', 'status': 'shortlisted'})
        self.stdout.write('[OK] Sarah Jones applied to Lifeguard (shortlisted)')

        Application.objects.get_or_create(candidate=cand3, job=job2,
            defaults={'cover_letter': 'Excited to operate rides', 'status': 'pending'})
        self.stdout.write('[OK] Mike Brown applied to Ride Operator (pending)')

        self.stdout.write(self.style.SUCCESS('Seed data complete!'))
