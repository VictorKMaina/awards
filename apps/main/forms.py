from django import forms
from apps.api.models import Project, User, Review

fields = ['title', 'description', 'site_url', 'landing_page_image']


def addClass(fields):
    dicts = []
    widgets = {}
    for field in fields:
        if field == 'site_url':
            dicts.append({field: forms.URLInput(attrs={'class': 'form-control'})})
        if field == 'password':
            dicts.append({field: forms.PasswordInput(attrs={'class': 'form-control'})})
        elif field != 'description':
            dicts.append({field: forms.TextInput(attrs={'class': 'form-control'})})
        else:
            dicts.append({field: forms.Textarea(attrs={'class': 'form-control'})})

    for dic in dicts:
        widgets.update(dic)
    return widgets


def addIntClass(fields):
    dicts = []
    widgets = {}
    for field in fields:
        if field == 'comment':
            dicts.append({field: forms.Textarea(
                attrs={'class': 'form-control'})})
        else:
            dicts.append({field: forms.NumberInput(
                attrs={'class': 'form-control', "min": '1', "max": '10'})})

    for dic in dicts:
        widgets.update(dic)
    return widgets

class NewProjectForm(forms.ModelForm):
    landing_page_image = forms.FileField()
    class Meta:
        model = Project
        fields = fields
        widgets = addClass(fields)

class SignupForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']
        widgets = addClass(fields)


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = addClass(fields)


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields=['design', 'usability', 'content', 'comment']
        widgets = addIntClass(fields)
