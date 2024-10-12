from django.urls import path

import core.views as core_views

app_name = "core"


def trigger_error(request):
    return 1 / 0


urlpatterns = [
    path("uploads/", core_views.upload_index, name="upload_index"),
    path("uploads/create/", core_views.create_upload, name="create_upload"),
    path(
        "uploads/<int:pk>/",
        core_views.upload_job_detail,
        name="upload_job_detail",
    ),
    path(
        "uploads/<int:upload_id>/delete/",
        core_views.delete_upload,
        name="delete_upload",
    ),
    path(
        "uploads/<int:upload_id>/create-uploaded-file/",
        core_views.create_uploaded_file,
        name="create_uploaded_file",
    ),
    path(
        "uploaded-files/<int:uploaded_file_id>/upload/",
        core_views.upload_file,
        name="upload_file",
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
    path("downloads/", core_views.my_downloads, name="my_downloads"),
    path("downloads/<str:filename>/", core_views.download_file, name="download_file"),
    path("debug/", trigger_error),
]
