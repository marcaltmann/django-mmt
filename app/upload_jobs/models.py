from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class UploadJob(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name=(_("Title")))
    description = models.TextField(blank=True, default="", verbose_name=_("Description"))
    language = models.CharField(max_length=255, blank=True, default="", verbose_name=_("Language"))
    make_available_on_platform = models.BooleanField(default=False, verbose_name=_("Make available on platform"))
    transcribe = models.BooleanField(default=False, verbose_name=_("Transcribe"))
    check_media_files = models.BooleanField(default=False, verbose_name=_("Check media files"))
    replace_existing_files = models.BooleanField(default=False, verbose_name=_("Replace existing files"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
