from django.contrib import admin

from .models import UploadedFile, UploadJob


class UploadedFileInline(admin.TabularInline):
    model = UploadedFile
    can_delete = False
    extra = 0


@admin.register(UploadJob)
class UploadJobAdmin(admin.ModelAdmin):
    inlines = [
        UploadedFileInline,
    ]
