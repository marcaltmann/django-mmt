import json

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from .forms import UploadJobForm
from .models import UploadJob
from uploaded_files.models import UploadedFile


@require_GET
@login_required
def upload_job_index(request):
    user = request.user
    upload_jobs = UploadJob.objects.filter(user=user).order_by("-created_at")
    data = [
        {
            "id": upload_job.id,
            "title": upload_job.title,
            "description": upload_job.description,
            "make_available_on_platform": upload_job.make_available_on_platform,
            "transcribe": upload_job.transcribe,
            "check_media_files": upload_job.check_media_files,
            "replace_existing_files": upload_job.replace_existing_files,
            "language": upload_job.language,
            "files_count": upload_job.uploaded_files.count(),
            "created_at": upload_job.created_at,
            "updated_at": upload_job.updated_at,
        }
        for upload_job in upload_jobs
    ]
    context = {"upload_jobs": upload_jobs}
    return render(request, "upload_jobs/upload_job_index.html", context)


@require_GET
@login_required
def upload_job_detail(request, pk):
    user = request.user
    upload_job = UploadJob.objects.get(pk=pk)

    if upload_job.user_id != user.id:
        return JsonResponse(
            {"message": "You are not allowed to update this file."}, status=403
        )

    uploaded_files = upload_job.uploaded_files.order_by("-created_at")

    job_data = {
        "id": upload_job.id,
        "title": upload_job.title,
        "description": upload_job.description,
        "make_available_on_platform": upload_job.make_available_on_platform,
        "transcribe": upload_job.transcribe,
        "check_media_files": upload_job.check_media_files,
        "replace_existing_files": upload_job.replace_existing_files,
        "language": upload_job.language,
        "created_at": upload_job.created_at,
        "updated_at": upload_job.updated_at,
    }

    file_data = [
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

    job_data["files"] = file_data

    return JsonResponse(job_data, safe=False)



@require_POST
@login_required
@csrf_exempt
def create_upload_job(request):
    json_data = json.loads(request.body)
    form = UploadJobForm(json_data)
    if form.is_valid():
        data = form.cleaned_data
        upload_job = UploadJob(
            title=data["title"],
            description=data["description"],
            language=data["language"],
            make_available_on_platform=data["make_available_on_platform"],
            transcribe=data["transcribe"],
            check_media_files=data["check_media_files"],
            replace_existing_files=data["replace_existing_files"],
        )
        upload_job.user = request.user
        upload_job.save()
        return JsonResponse({"id": upload_job.pk}, safe=False)
    else:
        return JsonResponse(form.errors, status=400)


@require_POST
@login_required
@csrf_exempt
def delete_upload_job(request, upload_job_id):
    upload_job = UploadJob.objects.get(pk=upload_job_id)
    user = request.user

    if upload_job.user_id != user.id:
        return JsonResponse(
            {"message": "You are not allowed to delete this upload job."}, status=403
        )

    upload_job.delete()
    return HttpResponse(status=204)


@require_POST
@login_required
@csrf_exempt
def create_uploaded_file(request, upload_job_id):
    user = request.user
    upload_job = UploadJob.objects.get(pk=upload_job_id)

    if upload_job is None:
        return JsonResponse({"message": "Upload job does not exist."}, status=404)

    if upload_job.user_id != user.id:
        return JsonResponse(
            {"message": "You are not allowed to create a file for this upload job."},
            status=403,
        )

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
        upload_job=upload_job,
        filename=filename,
        media_type=content_type,
        size=size,
    )

    return JsonResponse(
        {
            "id": file.id,
            "filename": file.filename,
        },
        status=201,
    )
