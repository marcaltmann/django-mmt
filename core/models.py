from django.conf import settings
from django.db import models


class UploadedFile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # file = models.FileField(upload_to='uploads/%Y/%m/%d/')
    filename = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    size = models.IntegerField(default=0)
    transferred = models.IntegerField(default=0)
    media_type = models.CharField(max_length=255, blank=True, null=False)
    checksum_server = models.CharField(max_length=255, blank=True, null=False)
    checksum_client = models.CharField(max_length=255, blank=True, null=False)

    def __str__(self):
        return self.filename
