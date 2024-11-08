from django.db import models
from django.db.models.signals import post_delete

from .filesystem import remove_file


class UploadedFile(models.Model):
    upload_job = models.ForeignKey(
        "upload_jobs.UploadJob", on_delete=models.CASCADE, related_name="uploaded_files"
    )
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
