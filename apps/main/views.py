from django.shortcuts import render
from django.contrib.auth import get_user_model, login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from ..api.emails.token import activation_token
from django.http import HttpResponse

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
