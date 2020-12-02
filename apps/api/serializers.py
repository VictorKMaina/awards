from rest_framework import serializers
from .models import User, Project, Review
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    is_superuser = serializers.BooleanField(default=False)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'is_superuser', 'is_staff', 'is_active']
    def create(self, validated_data):
        password = validated_data.get('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
