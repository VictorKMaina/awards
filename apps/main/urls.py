from . import views
from django.urls import path, re_path


urlpatterns = [
    path('', views.index, name="index"),
    path('logout/', views.log_out, name='logout'),
    path('activation/<uid>/<token>/', views.activate_account, name='activation'),
]
