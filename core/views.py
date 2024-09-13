from datetime import datetime, timezone
import mimetypes
import os

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse, FileResponse
from django.views.decorators.http import require_GET
from django.conf import settings

from .models import UploadedFile


@require_GET
@login_required
def my_uploads(request):
    user = request.user
    uploaded_files = UploadedFile.objects.filter(user=user)
    data = serializers.serialize("json", uploaded_files)
    return HttpResponse(data, content_type="application/json")


@require_GET
@login_required
def my_downloads(request):
    user = request.user
    username = user.username

    user_files_path = settings.BASE_DIR / "user_files"
    user_directory = user_files_path / username
    downloads_directory = user_directory / "downloads"

    if not downloads_directory.is_dir():
        return JsonResponse(
            {
                "message": "Downloads directory does not exist for the user.",
                "code": "no_downloads_directory",
            },
            status=500,
        )

    filepaths = [
        path
        for path in downloads_directory.iterdir()
        if path.is_file() and path.name != ".DS_Store"
    ]

    files_with_info = []
    for filepath in filepaths:
        media_type = mimetypes.guess_type(filepath)[0] or "application/octet-stream"
        statinfo = os.stat(filepath)
        file_info = {
            "filename": filepath.name,
            "type": media_type,
            "size": statinfo.st_size,
            "modified": datetime.fromtimestamp(statinfo.st_mtime, tz=timezone.utc),
        }
        files_with_info.append(file_info)

    return JsonResponse(files_with_info, safe=False)


@require_GET
@login_required
def download_file(request, filename):
    user = request.user
    username = user.username

    user_files_path = settings.BASE_DIR / "user_files"
    user_directory = user_files_path / username
    downloads_directory = user_directory / "downloads"

    # TODO: We should not return JSON here.
    if not downloads_directory.is_dir():
        return JsonResponse(
            {
                "message": "Downloads directory does not exist for the user.",
                "code": "no_downloads_directory",
            },
            status=404,
        )

    file_path = downloads_directory / filename

    if not file_path.is_file():
        return JsonResponse({"message": "File does not exist."}, status=404)

    # Use aiofiles in the future for async downloads.
    file = file_path.open("rb")
    return FileResponse(file, as_attachment=True, filename=filename)
