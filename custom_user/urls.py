from django.urls import path

import custom_user.views as views

app_name = "custom_user"

urlpatterns = [
    path("user/", views.user, name="user"),
    path("login/", views.sign_in, name="login"),
    path("logout/", views.sign_out, name="logout"),
]
