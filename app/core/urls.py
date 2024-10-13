from django.urls import path

import core.views as core_views

app_name = "core"


def trigger_error(request):
    return 1 / 0


urlpatterns = [
    # upload jobs
    path("uploads/", core_views.upload_job_index, name="upload_job_index"),
    path("uploads/create/", core_views.create_upload_job, name="create_upload_job"),
    path(
        "uploads/<int:pk>/",
        core_views.upload_job_detail,
        name="upload_job_detail",
    ),
    path(
        "uploads/<int:upload_job_id>/delete/",
        core_views.delete_upload_job,
        name="delete_upload_job",
    ),
    # uploaded files
    path(
        "uploads/<int:upload_job_id>/create-file/",
        core_views.create_uploaded_file,
        name="create_uploaded_file",
    ),
    path(
        "uploaded-files/<int:uploaded_file_id>/upload/",
        core_views.upload_uploaded_file,
        name="upload_uploaded_file",
    ),
    path(
        "uploaded-files/<int:uploaded_file_id>/update/",
        core_views.update_uploaded_file,
        name="update_uploaded_file",
    ),
    path(
        "uploaded-files/<int:uploaded_file_id>/delete/",
        core_views.delete_uploaded_file,
        name="delete_uploaded_file",
    ),
    # downloads -> move to own app
    path("downloads/", core_views.my_downloads, name="my_downloads"),
    path("downloads/<str:filename>/", core_views.download_file, name="download_file"),
    path("debug/", trigger_error),
]
