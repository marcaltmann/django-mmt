from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import UploadedFile
from .models import User, Profile


class UploadedFileInline(admin.TabularInline):
    model = UploadedFile
    fields = ("filename", "size", "media_type")
    readonly_fields = ("size",)
    max_num = 1
    extra = 0


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = [
        ProfileInline,
        UploadedFileInline,
    ]
