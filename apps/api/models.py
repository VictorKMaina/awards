from django.db import models
from cloudinary.models import CloudinaryField
from cloudinary.uploader import upload
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password, **kwargs):
        if not email:
            raise ValueError('Email required')
        if not first_name:
            raise ValueError('First name required')
        if not last_name:
            raise ValueError('Last name required')
        if not username:
            raise ValueError('Username required')
        if not password:
            raise ValueError('Password required')
        
        email = self.normalize_email(email)
        user = self.model(first_name=first_name, last_name=last_name, username=username, email=email, password=password, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, first_name, last_name, username, email, password, **kwargs):
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_active', True)

        if kwargs.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')
        if kwargs.get('is_active') is not True:
            raise ValueError('Superuser must have is_active=True')

        return self.create_user(first_name, last_name, username, email, password, **kwargs)

class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    profile_pic = models.URLField(
        default="https://res.cloudinary.com/victormainak/image/upload/v1606634881/icons8-male-user-100_zratap.png")
    bio = models.TextField(blank=True)
    website = models.URLField(null=True)
    social_media = models.JSONField(null=True)
    date_joined = models.CharField(max_length=255, default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def __str__(self):
        return f"{self.username} | ID: {self.id}"

    def upload_profile_pic(self, file):
        try:
            link = upload(file)
            print('CLOUDINARY URL: ', link.get('url'))
            self.profile_pic = link.get('url')
            self.save()

            details = {'public_id': link.get('public_id'), 'url':link.get('url')}
            return details
        except Exception as e:
            print("Cloudinary Error: ", e)


class Project(models.Model):
    title = models.CharField(max_length=255)
    landing_page_image = models.URLField()
    description = models.TextField()
    site_url = models.URLField(
        default='https://res.cloudinary.com/victormainak/image/upload/v1606635375/default_image_01_x3tuoe.png')
    average_rating = models.IntegerField(null=True)
    User = models.ForeignKey(User, on_delete=models.CASCADE)

    def upload_landing_page(self, file):
        try:
            link = upload(file)
            print('CLOUDINARY URL: ', link.get('url'))
            self.landing_page_image = link.get('url')
            self.save()

            details = {'public_id': link.get(
                'public_id'), 'url': link.get('url')}
            return details
        except Exception as e:
            print("Cloudinary Error: ", e)


class Review(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True)
    comment = models.TextField(blank=True)
