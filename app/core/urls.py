from django.urls import path

import core.views as core_views

app_name = "core"


def trigger_error(request):
    return 1 / 0


urlpatterns = [
    path("uploads/", core_views.my_uploads, name="my_uploads"),
    path("uploads/create/", core_views.create_upload, name="create_upload"),
    path("uploads/<int:upload_id>/upload/", core_views.upload_file, name="upload_file"),
    path(
        "uploads/<int:upload_id>/update/",
        core_views.update_upload,
        name="update_upload",
    ),
    path(
        "uploads/<int:upload_id>/delete/",
        core_views.delete_upload,
        name="delete_upload",
    ),
    path("downloads/", core_views.my_downloads, name="my_downloads"),
    path("downloads/<str:filename>/", core_views.download_file, name="download_file"),
    path("debug/", trigger_error),
]
