from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Candidate, JobListing, Skill, Application
from .forms import RegisterForm, CandidateForm


def get_profile(user):
    try:
        return UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return None


def home(request):
    total_jobs = JobListing.objects.filter(status='open').count()
    total_candidates = Candidate.objects.count()
    total_venues = JobListing.objects.values('venue_name').distinct().count()
    context = {
        'total_jobs': total_jobs,
        'total_candidates': total_candidates,
        'total_venues': total_venues,
    }
    return render(request, 'recruitment/home.html', context)


def about(request):
    return render(request, 'recruitment/about.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            role = form.cleaned_data['role']

            user = User.objects.create_user(
                username=username,
                email=email,
                password=password)
            UserProfile.objects.create(user=user, role=role)

            if role == 'candidate':
                Candidate.objects.create(user=user, first_name='',
                    last_name='', cv_summary='')

            messages.success(request, 'Registration successful!')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'recruitment/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'recruitment/login.html')


@login_required
def user_logout(request):
    logout(request)
    messages.success(request, 'Logged out successfully.')
    return redirect('home')


@login_required
def dashboard(request):
    profile = get_profile(request.user)
    if not profile:
        return render(request, 'recruitment/denied.html', status=403)

    if profile.role == 'recruiter':
        return redirect('dashboard_recruiter')
    elif profile.role == 'candidate':
        return redirect('dashboard_candidate')
    elif profile.role == 'manager':
        return redirect('dashboard_manager')
    return render(request, 'recruitment/denied.html', status=403)


@login_required
def dashboard_recruiter(request):
    profile = get_profile(request.user)
    if not profile or profile.role != 'recruiter':
        return render(request, 'recruitment/denied.html', status=403)

    my_jobs = JobListing.objects.filter(created_by=request.user)
    total_apps = Application.objects.filter(
        job__created_by=request.user).count()
    shortlisted = Application.objects.filter(
        job__created_by=request.user,
        status='shortlisted').count()

    context = {
        'my_jobs': my_jobs,
        'total_apps': total_apps,
        'shortlisted': shortlisted,
    }
    return render(request, 'recruitment/dashboard_recruiter.html', context)


@login_required
def dashboard_candidate(request):
    profile = get_profile(request.user)
    if not profile or profile.role != 'candidate':
        return render(request, 'recruitment/denied.html', status=403)

    try:
        candidate = Candidate.objects.get(user=request.user)
    except Candidate.DoesNotExist:
        candidate = None

    context = {'candidate': candidate}
    return render(request, 'recruitment/dashboard_candidate.html', context)


@login_required
def dashboard_manager(request):
    profile = get_profile(request.user)
    if not profile or profile.role != 'manager':
        return render(request, 'recruitment/denied.html', status=403)

    total_jobs = JobListing.objects.count()
    total_candidates = Candidate.objects.count()
    total_hired = Application.objects.filter(status='hired').count()

    context = {
        'total_jobs': total_jobs,
        'total_candidates': total_candidates,
        'total_hired': total_hired,
    }
    return render(request, 'recruitment/dashboard_manager.html', context)


@login_required
def candidates_list(request):
    profile = get_profile(request.user)
    if not profile or profile.role not in ['recruiter', 'manager']:
        return render(request, 'recruitment/denied.html', status=403)

    candidates = Candidate.objects.all()
    return render(request, 'recruitment/candidates_list.html',
        {'candidates': candidates})


@login_required
def candidate_detail(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    profile = get_profile(request.user)
    is_own = request.user == candidate.user

    if not is_own and (not profile or
        profile.role not in ['recruiter', 'manager']):
        return render(request, 'recruitment/denied.html', status=403)

    apps = Application.objects.filter(
        candidate=candidate) if is_own else []

    context = {'candidate': candidate, 'applications': apps}
    return render(request, 'recruitment/candidate_detail.html', context)


@login_required
def candidate_create(request):
    profile = get_profile(request.user)
    if not profile or profile.role != 'candidate':
        return render(request, 'recruitment/denied.html', status=403)

    try:
        candidate = Candidate.objects.get(user=request.user)
        return redirect('candidate_detail', pk=candidate.pk)
    except Candidate.DoesNotExist:
        pass

    if request.method == 'POST':
        form = CandidateForm(request.POST)
        if form.is_valid():
            candidate = form.save(commit=False)
            candidate.user = request.user
            candidate.save()
            messages.success(request, 'Profile created!')
            return redirect('candidate_detail', pk=candidate.pk)
    else:
        form = CandidateForm()
    return render(request, 'recruitment/candidate_form.html', {'form': form})


@login_required
def candidate_edit(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    if request.user != candidate.user:
        return render(request, 'recruitment/denied.html', status=403)

    if request.method == 'POST':
        form = CandidateForm(request.POST, instance=candidate)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('candidate_detail', pk=candidate.pk)
    else:
        form = CandidateForm(instance=candidate)
    return render(request, 'recruitment/candidate_form.html', {'form': form})


@login_required
def skills_manage(request):
    profile = get_profile(request.user)
    if not profile or profile.role != 'candidate':
        return render(request, 'recruitment/denied.html', status=403)

    try:
        candidate = Candidate.objects.get(user=request.user)
    except Candidate.DoesNotExist:
        messages.error(request, 'Create candidate profile first.')
        return redirect('candidate_create')

    if request.method == 'POST':
        skill_id = request.POST.get('skill_id')
        if skill_id:
            skill = get_object_or_404(Skill, pk=skill_id)
            if skill not in candidate.skills.all():
                candidate.skills.add(skill)
                messages.success(request, f'Added {skill.name}!')

        if 'remove_skill' in request.POST:
            remove_id = request.POST.get('remove_skill')
            skill = get_object_or_404(Skill, pk=remove_id)
            candidate.skills.remove(skill)
            messages.success(request, f'Removed {skill.name}!')

        return redirect('skills_manage')

    available_skills = Skill.objects.exclude(
        pk__in=candidate.skills.values_list('pk', flat=True))

    context = {
        'candidate': candidate,
        'available_skills': available_skills,
    }
    return render(request, 'recruitment/skills_manage.html', context)
