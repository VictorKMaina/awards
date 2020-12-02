from django.urls import path, re_path
from . import views

urlpatterns = [
    path('users/', views.UsersList.as_view(), name='list_users'),
    path('users/create-user/', views.CreateUser.as_view(), name='create_user'),
    path('projects/', views.ProjectsList.as_view(), name='list_projects'),
]
