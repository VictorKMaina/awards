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

User = get_user_model()

def get_token():
    requests.post

def index(request):
    user = request.user
    
    ctx = {}
    return render(request, 'main/index.html', ctx)


def single_project(request, project_id):
    ctx = {}
    return render(request, 'main/single_project.html', ctx)


def search_projects(request):
    ctx = {}
    return render(request, 'main/search_projects.html', ctx)


def create_project(request):
    form = NewProjectForm()
    ctx = {'form': form}
    return render(request, 'main/new_project.html', ctx)


def profile(request):
    # Check is profile belongs to logged in user to enable editing functionality
    ctx = {}
    return render(request, 'main/profile.html', ctx)


# Authentication Views
def loginUser(request):
    errors = []
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = form.data.get('username')
        password = form.data.get('password')
        user = User.objects.filter(username = username).first()
        if user is not None:
            if user.check_password(password):
                login(request, user)
                return redirect('/')
            else:
                errors.append("Incorrect username or password.")

    form = LoginForm()
    ctx = {"form": form, "errors": errors}
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


def confirm_account(request):
    """
    View that prompts user to check their mailbox for confirmation email. Redirects to login page.
    """
    ctx = {}
    return render(request, 'main/confirm_account.html', ctx)


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
        login(request)
        return HttpResponse('something found')
    else:
        return HttpResponse('nothing found')


def log_out(request):
    logout(request)
    return redirect('/')
