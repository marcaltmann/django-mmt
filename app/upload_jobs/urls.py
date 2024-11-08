from django.urls import path

import upload_jobs.views as views

app_name = "upload_jobs"


urlpatterns = [
    path("", views.upload_job_index, name="upload_job_index"),
    path("create/", views.create_upload_job, name="create_upload_job"),
    path("<int:pk>/", views.upload_job_detail, name="upload_job_detail"),
    path("<int:pk>/delete/", views.delete_upload_job, name="delete_upload_job"),
    path("<int:pk>/create-file/", views.create_uploaded_file, name="create_uploaded_file"),
]
