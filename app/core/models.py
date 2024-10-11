from django.conf import settings
from django.db import models
from django.db.models.signals import post_delete

from .filesystem import remove_file


class UploadJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    make_available_on_platform = models.BooleanField(default=False)
    transcribe = models.BooleanField(default=False)
    check_media_files = models.BooleanField(default=False)
    replace_existing_files = models.BooleanField(default=False)
    language = models.CharField(max_length=255, blank=True, default="")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class UploadedFile(models.Model):
    job = models.ForeignKey(UploadJob, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    size = models.IntegerField(default=0)
    transferred = models.IntegerField(default=0)
    media_type = models.CharField(max_length=255, blank=True, null=False)
    checksum_server = models.CharField(max_length=255, blank=True, null=False)
    checksum_client = models.CharField(max_length=255, blank=True, null=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.filename


post_delete.connect(
    remove_file, sender=UploadedFile, dispatch_uid="core.uploaded_file.remove_file"
)
