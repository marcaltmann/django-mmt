from pathlib import Path

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    pass


class Profile(models.Model):
    LOCALE_ENGLISH = "en"
    LOCALE_GERMAN = "de"
    LOCALE_CHOICES = (
        (LOCALE_ENGLISH, "English"),
        (LOCALE_GERMAN, "German"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True, null=False)
    locale = models.CharField(
        max_length=2,
        choices=LOCALE_CHOICES,
        default=LOCALE_ENGLISH,
    )

    def upload_path(self) -> Path:
        """Does not work with async."""
        username = self.user.username
        return settings.BASE_DIR / "user_files" / username / "uploads"

    def download_path(self) -> Path:
        """Does not work with async."""
        username = self.user.username
        return settings.BASE_DIR / "user_files" / username / "downloads"

    def __str__(self):
        return self.full_name
