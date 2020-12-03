from . import views
from django.urls import path, re_path


urlpatterns = [
    path('', views.index, name="index"),
    path('project/<int:project_id>/', views.single_project, name='single_project'),
    path('search/', views.search_projects, name='search_projects'),
    path('project/new/', views.create_project, name='create_project'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('auth/login/', views.login, name='login'),
    path('auth/signup/', views.signup, name='signup'),
    path('auth/confirm-account/', views.confirm_account, name='confirm-account'),
    path('auth/logout/', views.log_out, name='logout'),
    path('activation/<uid>/<token>/', views.activate_account, name='activation'),
]
