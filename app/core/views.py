from django.shortcuts import render
from django.http import HttpResponseServerError

from downloads.files import get_files_with_info


def welcome(request):
    user = request.user
    if user.is_authenticated:
        downloads_directory = user.download_path()
        try:
            files_with_info = get_files_with_info(downloads_directory)
        except FileNotFoundError:
            return HttpResponseServerError(
                "Downloads directory does not exist for the user."
            )
        upload_job_count = user.upload_jobs.count()
        download_job_count = len(files_with_info)
    else:
        upload_job_count = 0
        download_job_count = 0

    context = {
        "upload_job_count": upload_job_count,
        "download_file_count": download_job_count,
    }
    return render(request, "core/welcome.html", context)
