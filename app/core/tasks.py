from celery import shared_task
from django.conf import settings

from .filesystem import generate_file_md5
from .models import UploadedFile


@shared_task
def add(x: int, y: int) -> int:
    return x + y


@shared_task
def calculate_server_checksum(uploaded_file_id: int) -> str:
    uploaded_file = UploadedFile.objects.select_related("upload_job__user").get(
        pk=uploaded_file_id
    )
    user = uploaded_file.upload_job.user
    uploads_directory = settings.BASE_DIR / "user_files" / user.username / "uploads"
    file_path = uploads_directory / uploaded_file.filename

    checksum = generate_file_md5(file_path)
    UploadedFile.objects.filter(pk=uploaded_file_id).update(checksum_server=checksum)
    return checksum
