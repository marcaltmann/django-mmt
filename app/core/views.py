from django.shortcuts import render


def welcome(request):
    user = request.user
    upload_job_count = user.upload_jobs.count()

    context = {"upload_job_count": upload_job_count, "download_file_count": 13}
    return render(request, "core/welcome.html", context)
