from django.urls import path

import core.views as core_views

app_name = "core"

urlpatterns = [
    path("uploaded-files/", core_views.my_uploads, name="my_uploads"),
    path("downloads/", core_views.my_downloads, name="my_downloads"),
    path("downloads/<filename>/", core_views.download_file, name="download_file"),
]
