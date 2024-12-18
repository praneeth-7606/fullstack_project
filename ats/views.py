
import os
import requests
from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from PyPDF2 import PdfReader
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.middleware.cache import CacheMiddleware
from django.views.decorators.cache import cache_control
from .forms import ResumeUploadForm, ATSForm, SignUpForm, LoginForm
from .models import UserProfile
from decouple import config

# Hugging Face API constants
HUGGING_FACE_API = config('HUGGING_FACE_API')
API_TOKEN = config('API_TOKEN')


# Utility function to extract text from a PDF
def extract_text_from_pdf(file):
    """Extract text from a PDF file."""
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

# Utility function to call Hugging Face API
def call_hugging_face_api(resume_text, job_description):
    """Send request to Hugging Face API and calculate similarity score."""
    headers = {"Authorization": f"Bearer {API_TOKEN}"}
    data = {
        "inputs": {
            "source_sentence": resume_text,
            "sentences": [job_description],
        }
    }
    response = requests.post(HUGGING_FACE_API, headers=headers, json=data)
    
    if response.status_code == 200:
        similarities = response.json()  # Expecting a list of similarity scores
        if similarities:
            return round(similarities[0] * 100, 2)  # Convert to percentage
    return None

# ATS score calculation logic
# def calculate_score(parsed_resume_text, job_description):
#     """Fallback similarity score calculation."""
#     resume_words = set(parsed_resume_text.lower().split())
#     job_words = set(job_description.lower().split())
#     match_count = len(resume_words & job_words)
#     return round((match_count / len(job_words)) * 100, 2)
from collections import Counter

def calculate_score(parsed_resume_text, job_description):
  
    resume_tokens = parsed_resume_text.lower().split()
    job_tokens = job_description.lower().split()

    if not job_tokens:
        return 0.0  

    resume_word_count = Counter(resume_tokens)
    match_count = 0

   
    for word in job_tokens:
        if resume_word_count[word] > 0:
            match_count += 1

    score = (match_count / len(job_tokens)) * 100
    return round(score, 2)


# View for calculating ATS score
def calculate_ats_score(request):
    if request.method == "POST":
        resume_file = request.FILES.get('resume')
        job_description = request.POST.get('jobDescription')

        if not resume_file or not job_description:
            messages.error(request, "Please provide both a resume and a job description.")
            return redirect('mainpage')

        # Save the resume file
        file_path = default_storage.save(f'resumes/{resume_file.name}', resume_file)
        file_full_path = os.path.join(settings.MEDIA_ROOT, file_path)

        try:
            # Extract text from the uploaded resume
            with open(file_full_path, 'rb') as file:
                resume_text = extract_text_from_pdf(file)

            # Call Hugging Face API to calculate similarity score
            ats_score = call_hugging_face_api(resume_text, job_description)

            # Fallback logic if API fails
            if ats_score is None:
                ats_score = calculate_score(resume_text, job_description)

            messages.success(request, f"ATS Score Calculated: {ats_score}")
            return render(request, 'mainpage.html', {'ats_score': ats_score})

        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        finally:
            # Clean up saved file
            if os.path.exists(file_full_path):
                os.remove(file_full_path)

    return render(request, 'home.html')


# Signup view
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create User instance
            user = User.objects.create_user(
                username=form.cleaned_data['email'],  # Using email as username
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )
            # Create UserProfile instance
            UserProfile.objects.create(
                user=user,
                name=form.cleaned_data['name'],
                phone_number=form.cleaned_data['phone_number']
            )
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})




def login_required_message(view_func):
    """Custom login_required decorator that shows a message."""
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Please log in to navigate to the main page.")
            return redirect('login')  # Redirect to the login page
        return view_func(request, *args, **kwargs)
    return wrapped_view



# Login view
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                messages.success(request, 'Logged in successfully!')
                next_page = request.GET.get('next', 'mainpage')
                return redirect(next_page)
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})



@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required
def logout_view(request):
    """Logout user and prevent access to cached pages."""
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('login')


# Home view
def home(request):
    return render(request, 'home.html')
def about(request):
    return render(request,'about.html')
@login_required(login_url='login')  # Redirects to 'login' if not logged in
def mainpage(request):
    return render(request, 'mainpage.html')

def rules(request):
    return render(request,'rules.html')
def hihello(request):
    return render(request,'hihello.html')


