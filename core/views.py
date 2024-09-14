from datetime import datetime, timezone
import json
import logging
import mimetypes
import os
import threading

import aiofiles
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, FileResponse, StreamingHttpResponse
from django.views.decorators.http import require_GET, require_POST
from django.conf import settings

from .models import UploadedFile

logger = logging.getLogger(__name__)


def debug(msg):
    logger.info(msg)
    print(msg)


@require_GET
@login_required
def my_uploads(request):
    user = request.user
    uploaded_files = UploadedFile.objects.filter(user=user).order_by("-created_at")
    data = [
        {
            "id": file.id,
            "filename": file.filename,
            "content_type": file.media_type,
            "size": file.size,
            "state": "created",
            "created": file.created_at,
            "checksum_client": file.checksum_client,
            "checksum_server": file.checksum_server,
        }
        for file in uploaded_files
    ]

    return JsonResponse(data, safe=False)


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
    file_path = downloads_directory / filename

    # TODO: We should not return JSON here.
    if not file_path.is_file():
        return JsonResponse({"message": "File does not exist."}, status=404)

    debug(f"Requested {filename} which stats {os.stat(file_path)=}.")

    response = StreamingHttpResponse(
        file_data(file_path), content_type="application/octet-stream"
    )
    response["Content-Disposition"] = f'attachment; filename="{filename}"'
    return response


async def file_data(file_path, chunk_size=65536):
    debug(f"Current threads are {threading.active_count()} opening file {file_path}.")
    async with aiofiles.open(file_path, mode="rb") as f:
        teller = 0
        while chunk := await f.read(chunk_size):
            teller += 1
            if teller % 1000 == 0:
                debug(
                    f"Current threads are {threading.active_count()} yielding chunk nr.{teller}."
                )
            yield chunk


@require_POST
@login_required
def create_upload(request):
    json_data = json.loads(request.body)
    filename = json_data["filename"]
    content_type = json_data["content_type"]
    size = json_data["size"]

    error = None
    if not filename:
        error = "Filename is required."
    elif not content_type:
        error = "Content_type is required."
    elif not size:
        error = "Size is required."

    if error:
        return JsonResponse({"message": error}, status=400)

    file = UploadedFile.objects.create(
        user=request.user,
        filename=filename,
        media_type=content_type,
        size=size,
    )

    return JsonResponse({
        "id": file.id,
        "filename": file.filename,
    }, status=201)


@require_POST
@login_required
def update_upload(request, upload_id):
    upload = UploadedFile.objects.get(id=upload_id)
    if upload.user != request.user:
        return JsonResponse({"message": "You are not allowed to update this file."}, status=403)

    json_data = json.loads(request.body)
    checksum_client = json_data["checksum_client"]

    if checksum_client:
        upload.checksum_client = checksum_client
        upload.save()

    return JsonResponse({"message": "Upload successfully updated."}, status=200)


@require_POST
@login_required
def delete_upload(request, upload_id):
    upload = UploadedFile.objects.get(id=upload_id)

    if upload.user != request.user:
        return JsonResponse({"message": "You are not allowed to delete this file."}, status=403)

    upload.delete()
    return HttpResponse(status=204)
