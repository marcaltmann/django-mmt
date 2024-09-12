from django.urls import path

import core.views as core_views

app_name = 'core'

urlpatterns = [
    path("uploaded-files/", core_views.my_uploads, name="my_uploads"),
]
