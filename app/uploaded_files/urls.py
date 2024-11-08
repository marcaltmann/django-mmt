from django.urls import path

import uploaded_files.views as views

app_name = "uploaded_files"

urlpatterns = [
    path("<int:pk>/upload/", views.upload, name="upload"),
    path("<int:pk>/update/", views.update, name="update"),
    path("<int:pk>/delete/", views.delete, name="delete"),
]
