from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode

from ..api.emails.token import activation_token

def index(request):
    ctx = {}
    return render(request, 'main/index.html', ctx)

def single_project(request):
    ctx = {}
    return render(request, 'main/single_project.html', ctx)

def search_projects(request):
    ctx = {}
    return render(request, 'main/search_projects.html', ctx)

def create_project(request):
    ctx = {}
    return render(request, 'main/index.html', ctx)

def profile(request):
    # Check is profile belongs to logged in user to enable editing functionality
    ctx = {}
    return render(request, 'main/index.html', ctx)


# Authentication Views
def login(request):
    ctx = {}
    return render(request, 'auth/login.html', ctx)

def signup(request):
    ctx = {}
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
        login(request, user)
        return HttpResponse('something found')
    else:
        return HttpResponse('nothing found')

def log_out(request):
    logout(request)
    return HttpResponse('logged out')
