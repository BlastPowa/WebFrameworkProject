from django import forms
from django.contrib.auth.models import User
from .models import Candidate, JobListing, Application, Skill


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Username'}))
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}))
    role = forms.ChoiceField(
        choices=[
            ('candidate', 'Candidate'),
            ('recruiter', 'Recruiter'),
            ('manager', 'Manager'),
        ],
        widget=forms.Select(attrs={'class': 'form-select'}))

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('password') != cleaned_data.get('password2'):
            raise forms.ValidationError('Passwords do not match.')
        return cleaned_data


class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name', 'age', 'experience_years',
                  'cv_summary', 'availability', 'profile_image']
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control'}),
            'age': forms.NumberInput(
                attrs={'class': 'form-control'}),
            'experience_years': forms.NumberInput(
                attrs={'class': 'form-control'}),
            'cv_summary': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4}),
            'availability': forms.Select(
                attrs={'class': 'form-select'}),
            'profile_image': forms.FileInput(
                attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class JobListingForm(forms.ModelForm):
    class Meta:
        model = JobListing
        fields = ['title', 'venue_name', 'venue_type', 'description',
                  'employment_type', 'salary', 'status', 'venue_image']
        widgets = {
            'title': forms.TextInput(
                attrs={'class': 'form-control'}),
            'venue_name': forms.TextInput(
                attrs={'class': 'form-control'}),
            'venue_type': forms.Select(
                attrs={'class': 'form-select'}),
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 4}),
            'employment_type': forms.Select(
                attrs={'class': 'form-select'}),
            'salary': forms.NumberInput(
                attrs={'class': 'form-control'}),
            'status': forms.Select(
                attrs={'class': 'form-select'}),
            'venue_image': forms.FileInput(
                attrs={'class': 'form-control', 'accept': 'image/*'}),
        }


class ApplicationForm(forms.ModelForm):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Full Name'}))
    age = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={'class': 'form-control', 'placeholder': 'Age'}))
    experience = forms.CharField(
        max_length=500,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Years of Experience'}))
    skills_text = forms.CharField(
        max_length=500,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Your Skills (comma separated)'}))

    class Meta:
        model = Application
        fields = ['cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(
                attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Cover Letter'}),
        }


class ApplicationStatusForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['status']
        widgets = {
            'status': forms.Select(
                attrs={'class': 'form-select'}),
        }
