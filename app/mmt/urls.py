from django.conf import settings
from django.conf.urls.i18n import i18n_patterns

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("api/", include("core.urls")),
    path("api/auth/", include("custom_user.urls")),
    path("", include("django_vite_plugin.urls")),
]

urlpatterns += i18n_patterns(
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("", include("pages.urls")),
)

if settings.DEBUG:
    urlpatterns.append(path("__debug__/", include("debug_toolbar.urls")))
