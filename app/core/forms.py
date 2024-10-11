from django import forms

from .models import UploadJob, UploadedFile


class UploadJobForm(forms.ModelForm):
    class Meta:
        model = UploadJob
        fields = [
            "title",
            "description",
            "make_available_on_platform",
            "transcribe",
            "check_media_files",
            "replace_existing_files",
            "language",
        ]


class UploadedFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ["filename", "media_type", "size"]
