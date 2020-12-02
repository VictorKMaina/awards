from django.urls import path, re_path
from . import views

urlpatterns = [
    path('users/', views.Users.as_view(), name='users'),
    path('projects/', views.Projects.as_view(), name='projects'),
    path('reviews/', views.Reviews.as_view(), name='reviews')
]
