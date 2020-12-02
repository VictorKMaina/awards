from django.shortcuts import redirect, render
from django.contrib.auth import get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from ..api.emails.token import activation_token
from django.http import HttpResponse

@login_required(login_url='login/')
def index(request):
    print('USER: ', request.user)
    return HttpResponse('nothing')

def log_out(request):
    logout(request)
    return HttpResponse('logged out')

def activate_account(request, uid, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uid))
        user = User.objects.get(pk=uid)
    except:
        user = None

    ctx = {'uid': uid, 'token': token}
    if user is not None and activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('something found')
    else:
        return HttpResponse('nothing found')
