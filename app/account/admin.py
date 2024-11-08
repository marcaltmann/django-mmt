from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [
        ProfileInline,
    ]
