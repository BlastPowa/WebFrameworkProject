from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import (
    JobListing, Candidate, Application, UserProfile
)
from .forms import JobListingForm, ApplicationForm, ApplicationStatusForm


def get_profile(user):
    try:
        return UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        return None


def jobs_list(request):
    jobs = JobListing.objects.filter(status='open')
    return render(request, 'recruitment/jobs_list.html', {'jobs': jobs})


def job_detail(request, pk):
    job = get_object_or_404(JobListing, pk=pk)
    profile = get_profile(request.user)
    user_applied = False
    applicants = []

    if request.user.is_authenticated:
        try:
            candidate = Candidate.objects.get(user=request.user)
            user_applied = Application.objects.filter(
                candidate=candidate, job=job).exists()
        except Candidate.DoesNotExist:
            pass

        if profile and profile.role in ['recruiter', 'manager']:
            applicants = Application.objects.filter(job=job)

    context = {
        'job': job,
        'user_applied': user_applied,
        'applicants': applicants,
    }
    return render(request, 'recruitment/job_detail.html', context)


@login_required
def job_create(request):
    profile = get_profile(request.user)
    if not profile or profile.role != 'recruiter':
        return render(request, 'recruitment/denied.html', status=403)

    if request.method == 'POST':
        form = JobListingForm(request.POST, request.FILES)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            messages.success(request, 'Job created!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobListingForm()
    return render(request, 'recruitment/job_form.html', {'form': form})


@login_required
def job_edit(request, pk):
    job = get_object_or_404(JobListing, pk=pk)
    profile = get_profile(request.user)
    if job.created_by != request.user:
        return render(request, 'recruitment/denied.html', status=403)

    if request.method == 'POST':
        form = JobListingForm(request.POST, request.FILES, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated!')
            return redirect('job_detail', pk=job.pk)
    else:
        form = JobListingForm(instance=job)
    return render(request, 'recruitment/job_form.html', {'form': form})


@login_required
def apply_job(request, pk):
    job = get_object_or_404(JobListing, pk=pk)
    profile = get_profile(request.user)
    if not profile or profile.role != 'candidate':
        return render(request, 'recruitment/denied.html', status=403)

    try:
        candidate = Candidate.objects.get(user=request.user)
    except Candidate.DoesNotExist:
        messages.error(request, 'Create candidate profile first.')
        return redirect('candidate_create')

    existing = Application.objects.filter(
        candidate=candidate, job=job).first()
    if existing:
        messages.error(request, 'Already applied!')
        return redirect('job_detail', pk=job.pk)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save(commit=False)
            app.candidate = candidate
            app.job = job
            app.save()
            messages.success(request, 'Application submitted!')
            return redirect('my_applications')
    else:
        form = ApplicationForm()

    context = {'job': job, 'form': form}
    return render(request, 'recruitment/apply_form.html', context)


@login_required
def my_applications(request):
    profile = get_profile(request.user)
    if not profile or profile.role != 'candidate':
        return render(request, 'recruitment/denied.html', status=403)

    try:
        candidate = Candidate.objects.get(user=request.user)
        apps = Application.objects.filter(candidate=candidate)
    except Candidate.DoesNotExist:
        apps = []

    return render(request, 'recruitment/my_applications.html',
        {'applications': apps})


@login_required
def application_update(request, pk):
    app = get_object_or_404(Application, pk=pk)
    profile = get_profile(request.user)
    if app.job.created_by != request.user:
        return render(request, 'recruitment/denied.html', status=403)

    if request.method == 'POST':
        form = ApplicationStatusForm(request.POST, instance=app)
        if form.is_valid():
            form.save()
            messages.success(request, 'Application updated!')
            return redirect('job_detail', pk=app.job.pk)
    else:
        form = ApplicationStatusForm(instance=app)

    return render(request, 'recruitment/application_form.html',
        {'form': form, 'application': app})
