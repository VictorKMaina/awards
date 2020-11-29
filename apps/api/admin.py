from django.contrib import admin
from .models import User, Project, Review
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea


class UserAdminConfig(UserAdmin):
    ordering = ('-date_joined',)
    list_display = ('email', 'username', 'first_name',
                    'last_name', 'is_active', 'is_staff')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    fieldsets = (
        (None, {'fields': ('email', 'username', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Personal', {'fields': ('bio',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_active', 'is_staff')
        }),
    )


# Register your models here.
admin.site.register(User, UserAdminConfig)
admin.site.register(Project)
admin.site.register(Review)
