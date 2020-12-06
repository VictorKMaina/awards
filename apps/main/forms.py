from django import forms
from apps.api.models import Project, User

fields = ['title', 'description', 'site_url', 'landing_page_image']


def addClass(fields):
    dicts = []
    widgets = {}
    for field in fields:
        if field != 'description':
            dicts.append({field: forms.TextInput(attrs={'class': 'form-control'})})
        else:
            dicts.append({field: forms.Textarea(attrs={'class': 'form-control'})})

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
