from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
import json

from ..api.emails.token import activation_token
from .forms import NewProjectForm, SignupForm, LoginForm
import requests
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.authtoken.models import Token
from apps.api.models import Project, Review
import random
from apps.main.project_review import review_average
from rest_framework.decorators import api_view
from apps.main.forms import ReviewForm
from itertools import chain

User = get_user_model()

def index(request):
    user = request.user
    projects = Project.objects.all()

    if len(projects) > 0:
        featured = random.choice(projects)
        ctx = {"projects": projects, 'featured': featured}
        return render(request, 'main/index.html', ctx)

    ctx = {"projects": projects}    
    return render(request, 'main/index.html', ctx)


# @api_view(['GET', 'POST'])
def single_project(request, project_id):
    user = request.user
    project = Project.objects.filter(id = project_id).first()
    reviews = Review.objects.filter(project = project).all()
    average_review = review_average(project)

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = {**request.POST, 'project':project.id}
            url = "http://"+str(get_current_site(request)) + "/api/reviews/"
            token = Token.objects.filter(user=user).first()
            headers = {"Authorization":f"Token {token}"}
            data = requests.post(url, review, headers=headers)

            average_review = review_average(project)
            ctx = {"project":project, "average_review":average_review, "form":form, "reviews":reviews}
            return render(request, 'main/single_project.html', ctx)

    form = ReviewForm()
    ctx = {"project":project, "average_review":average_review, "form":form, "reviews":reviews}
    return render(request, 'main/single_project.html', ctx)


def search_projects(request):
    user = request.user
    query = request.GET.get('query')
    
    by_user = Project.objects.filter(user__username__icontains = query)
    by_title = Project.objects.filter(title__icontains=query) 
    by_description = Project.objects.filter(description__icontains=query)
    projects = list(dict.fromkeys(chain(by_title, by_user, by_description)))

    ctx = {'projects':projects}
    return render(request, 'main/search_projects.html', ctx)

@login_required(login_url='auth/login/')
def create_project(request):
    user = request.user
    errors = []
    if request.method == 'POST':
        form = NewProjectForm(request.POST, request.FILES)
        image = request.FILES.get('landing_page_image')
        title = (form.data.get('title'))
        description = (form.data.get('description'))
        site_url = (form.data.get('site_url'))

        new_project = Project.objects.create(title=title, description=description, site_url=site_url, user=user)

        new_project.upload_landing_page(image)

        return redirect('/')
    form = NewProjectForm()
    ctx = {"form": form, "errors": errors}
    return render(request, 'main/new_project.html', ctx)


def profile(request, username):
    # Check is profile belongs to logged in user to enable editing functionality
    ctx = {}
    return render(request, 'main/profile.html', ctx)


# Authentication Views
def loginUser(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = form.data.get('username')
        password = form.data.get('password')
        user = User.objects.filter(username = username).first()
        if user is not None and user.is_active:
            if user.check_password(password):
                url = "http://"+str(get_current_site(request)) + "/api/users/auth-token/"
                requests.post(url, form.data)
                login(request, user)
                return redirect('/')
            else:
                errors = "Incorrect username or password."
                ctx = {"form": form, "errors": errors}
                return render(request, 'auth/login.html', ctx)
        else:
            errors = "Incorrect username or password."
            ctx = {"form": form, "errors": errors}
            return render(request, 'auth/login.html', ctx)

    form = LoginForm()
    ctx = {"form": form}
    return render(request, 'auth/login.html', ctx)


def signup(request):
    errors = []
    if request.method == 'POST':
        form = SignupForm(request.POST)
        url = "http://"+str(get_current_site(request)) + "/api/users/"
        data = requests.post(url, form.data)
        response = json.loads(data.content)
        user_id = response.get('id')
        if user_id is not None:
            return redirect("/auth/login")
        else:
            if response.get('username'):
                errors.append(response.get('username')[0])
            if response.get('email'):
                errors.append(response.get('email')[0])
    form = SignupForm()
    ctx = {"form": form, "errors":errors}
    return render(request, 'auth/signup.html', ctx)


def activate_account(request, uid, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('/auth/login/')
    else:
        return redirect('/auth/signup/')


@login_required(login_url='auth/login/')
def log_out(request):
    logout(request)
    return redirect('/')
