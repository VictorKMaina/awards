from django.shortcuts import render
from rest_framework import status
# from .permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .emails.activate_email import send_activation_email
from .models import Project, Review, User
from .serializers import ProjectSerializer, UserSerializer
from django.contrib.auth import get_user_model, login
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from .emails.token import activation_token
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse


class CreateUser(APIView):
    """
    Create new user instance
    """
    permission_classes = (AllowAny,)

    def post(self, request):
        serializers = UserSerializer(data=request.data)
        
        if serializers.is_valid():
            user = serializers.save()
            send_activation_email(request, user)

            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class UsersList(APIView):
    """
    Return list of users
    """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def get(self, request):
        users = User.objects.all()
        serializers = UserSerializer(users, many = True)

        return Response(serializers.data)

class ProjectsList(APIView):
    """
    Create a new user instance
    """
    def get(self, request):
        projects = Project.objects.all()
        serializers = ProjectSerializer(projects, many=True)

        return Response(serializers.data)
