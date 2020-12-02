from . import views
from django.urls import path, re_path


urlpatterns = [
    path('activation/<uid>/<token>/', views.activate_account, name='activation'),
]
