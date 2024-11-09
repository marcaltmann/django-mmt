from datetime import datetime, timezone
import logging
import mimetypes
import os
import threading

import aiofiles
from django.contrib.auth.decorators import login_required
from django.http import (
    StreamingHttpResponse,
    HttpResponseServerError,
    HttpResponseNotFound,
    HttpResponse,
)
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_http_methods

from account.models import Profile

logger = logging.getLogger(__name__)


def debug(msg):
    logger.info(msg)
    print(msg)


@require_GET
@login_required
def download_index(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user_id=user.id)
    downloads_directory = profile.download_path()
    if not downloads_directory.is_dir():
        return HttpResponseServerError(
            "Downloads directory does not exist for the user."
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

    context = {"files": files_with_info}

    return render(request, "downloads/download_index.html", context)


@require_http_methods(["GET", "DELETE"])
@login_required
@csrf_exempt
def download_detail(request, filename):
    user = request.user
    downloads_directory = user.profile.download_path()
    file_path = downloads_directory / filename

    if not file_path.is_file():
        return HttpResponseNotFound("File does not exist.")

    if request.method == "GET":
        # Download the file
        debug(f"Requested {filename} which stats {os.stat(file_path)=}.")

        response = StreamingHttpResponse(
            file_data(file_path), content_type="application/octet-stream"
        )
        response["Content-Disposition"] = f'attachment; filename="{filename}"'
        return response
    elif request.method == "DELETE":
        # Delete the file
        file_path.unlink()

        return HttpResponse(status=200)


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
