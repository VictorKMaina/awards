from django.contrib.auth import get_user_model, login
from django.http import HttpResponseRedirect
from django.http.response import HttpResponse
from django.shortcuts import render
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from rest_framework import status
# from .permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .emails.activate_email import send_activation_email
from .emails.token import activation_token
from .models import Project, Review, User
from .serializers import ProjectSerializer, UserSerializer, ReviewSerializer


class Users(APIView):
    """
    GET: Return list of users
    POST: Create new user
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        users = User.objects.all()
        serializers = UserSerializer(users, many = True)

        return Response(serializers.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        serializers = UserSerializer(data=request.data)

        if serializers.is_valid():
            user = serializers.save()
            send_activation_email(request, user)

            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class Projects(APIView):
    """
    GET: Return list of all projects or of projects by single user
    POST: Create a new project
    PATCH: Update a project
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        # Return a single project instance by project id
        if request.GET.get('id'):
            project = Project.objects.filter(id = request.GET['id']).first()
            serializers = ProjectSerializer(project)

            return Response(data=serializers.data, status=status.HTTP_200_OK)
        
        # Return a queryset of projects based on user id
        if request.GET.get('username'):
            user = User.objects.filter(username=request.GET['username']).first()
            projects = Project.objects.filter(user=user).all()
    
            if len(projects) > 0:
                serializers = ProjectSerializer(projects, many=True)
                return Response(serializers.data, status=status.HTTP_200_OK)
            return Response({"null": True}, status=status.HTTP_200_OK)
        
        # Return all project instances
        else:
            projects = Project.objects.all()
            serializers = ProjectSerializer(projects, many=True)

            return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = {**request.data.dict(), **{'user': request.user.pk}}
        serializers = ProjectSerializer(data = data)

        if serializers.is_valid():
            new_project = serializers.save(user = request.user)
            new_project.save()

            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        try:
            project = Project.objects.filter(pk = request.data['id']).first()
        except:
            return Response(data={'message':'Please enter valid project id.'})

        if project is not None:
            serializers = ProjectSerializer(project, data=request.data, partial=True)
            check_user = User.objects.filter(pk = project.user.id).first()
            if serializers.is_valid():
                if check_user == request.user:
                    serializers.save()
                    return Response(data=serializers.data, status=status.HTTP_206_PARTIAL_CONTENT)
                return Response(data={'message':'You are not authorized to make this request.'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(data=serializers.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(data={'null':True, 'message':'Project not found.'}, status=status.HTTP_404_NOT_FOUND)

class Reviews(APIView):
    """
    GET:
    POST:
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        if request.GET.get('project_id'):
            # Return reviews by project
            reviews = Review.objects.filter(project=request.GET.get('project_id')).all()
            
        else:
            reviews = Review.objects.all()

        serializers = ReviewSerializer(reviews, many=True)
        return Response(data = serializers.data)        

    def post(self, request):
        data = {**request.data.dict(), **{'user': request.user.pk}}
        serializers = ReviewSerializer(data=data)

        if serializers.is_valid():
            new_review = serializers.save(user=request.user)
            new_review.save()

            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)
