import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _
import dotenv


dotenv.read_dotenv("../.env.dev")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    default="django-insecure-v&me14sv4_mbo_s9xi_r^@f)h7#8v*&6&gp+y2#jp7)5vfl64&",
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(int(os.environ.get("DEBUG", default=1)))

ALLOWED_HOSTS = os.environ.get(
    "DJANGO_ALLOWED_HOSTS", default="localhost 127.0.0.1"
).split(" ")

INTERNAL_IPS = [
    "127.0.0.1",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
CORS_ALLOW_CREDENTIALS = True


# Application definition

INSTALLED_APPS = [
    "account.apps.AccountConfig",
    "core.apps.CoreConfig",
    "downloads.apps.DownloadsConfig",
    "pages.apps.PagesConfig",
    "upload_jobs.apps.UploadJobsConfig",
    "uploaded_files.apps.UploadedFilesConfig",
    "django_htmx",
    "django_extensions",
    "corsheaders",
    "widget_tweaks",
    "debug_toolbar",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.humanize",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    "django_vite_plugin",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_htmx.middleware.HtmxMiddleware",
]

ROOT_URLCONF = "mmt.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "mmt.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "OPTIONS": {
            "read_default_file": str(BASE_DIR / "my.cnf"),
            "isolation_level": "read committed",
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

USE_I18N = True
LANGUAGES = [
    ("de", _("German")),
    ("en", _("English")),
]
LANGUAGE_CODE = "en-us"
LOCALE_PATHS = (BASE_DIR / "locale",)
USE_TZ = True
TIME_ZONE = "UTC"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "build"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "account:profile"
LOGOUT_REDIRECT_URL = "welcome"
AUTH_USER_MODEL = "account.User"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_PORT = os.environ.get("EMAIL_PORT")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")

# CELERY_BACKEND = "redis://localhost"
CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", default="redis://localhost")
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True
