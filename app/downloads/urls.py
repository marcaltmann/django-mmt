from django.urls import path

import downloads.views as views

app_name = "downloads"

urlpatterns = [
    path("", views.download_index, name="download_index"),
    path("<str:filename>/", views.download_detail, name="download_detail"),
]
