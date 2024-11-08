from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", include("django_vite_plugin.urls")),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("account/", include("django.contrib.auth.urls")),
    path("account/", include("account.urls")),
    path("", include("core.urls")),
    path("downloads/", include("downloads.urls")),
    path("", include("pages.urls")),
)

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
