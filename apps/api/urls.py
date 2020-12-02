from django.urls import path, re_path
from . import views

urlpatterns = [
    path('users/', views.AllUsersList.as_view(), name='all_users'),
    path('projects/', views.Projects.as_view(), name='all_projects'),
]
