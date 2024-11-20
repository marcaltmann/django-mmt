import json

import aiofiles
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpResponseNotFound, Http404
from django.views.decorators.http import require_POST

from .models import UploadedFile
from .tasks import calculate_server_checksum, send_file_uploaded_emails


@require_POST
@login_required
async def upload(request, pk):
    uploaded_file = await UploadedFile.objects.select_related("upload_job").aget(pk=pk)
    upload_job = uploaded_file.upload_job

    user = await request.auser()
    if upload_job.user_id != user.id:
        return JsonResponse(
            {"message": "You are not allowed to upload this file."}, status=403
        )

    # User#upload_path does not work with async.
    upload_path = settings.BASE_DIR / "user_files" / user.username / "uploads"
    file_path = upload_path / uploaded_file.filename

    file = request.FILES["file"]
    await handle_uploaded_file(file, file_path)

    send_file_uploaded_emails.delay(user.id, uploaded_file.filename)
    calculate_server_checksum.delay(pk)

    return JsonResponse({"success": True})


async def handle_uploaded_file(file, file_path):
    async with aiofiles.open(file_path, "wb") as f:
        for chunk in file.chunks():
            await f.write(chunk)


@require_POST
@login_required
def update(request, pk):
    uploaded_file = UploadedFile.objects.select_related("upload_job").get(pk=pk)
    upload_job = uploaded_file.upload_job
    if upload_job.user_id != request.user.id:
        return JsonResponse(
            {"message": "You are not allowed to update this file."}, status=403
        )

    json_data = json.loads(request.body)
    checksum_client = json_data["checksum_client"]

    if not checksum_client:
        return JsonResponse({"message": "checksum_client is required."}, status=400)

    uploaded_file.checksum_client = checksum_client
    uploaded_file.save()

    return JsonResponse({"message": "Upload successfully updated."}, status=200)


@require_POST
@login_required
def delete(request, pk):
    user = request.user
    uploaded_file = UploadedFile.objects.get(pk=pk, upload_job__user_id=user.id)
    uploaded_file.delete()

    # Remove actual file.
    uploads_directory = user.upload_path()
    file_path = uploads_directory / uploaded_file.filename
    try:
        file_path.unlink()
    except FileNotFoundError:
        print(f"File {uploaded_file.filename} does not exist.")

    return HttpResponse(status=200)
