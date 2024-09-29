import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = str(os.getenv("SECRET_KEY"))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['api.localhost', 'localhost', 'api.mysite', 'mysite']
ALLOWED_HOSTS: list[str] = ["*"]


# Application definition

INSTALLED_APPS = [
    "web.admin",
    "web.user",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "adminsortable2",
    "colorfield",
    "ckeditor",
    "web.site_statistics",
    "web.catalog",
    "web.common",
    "web.account",
    "web.settings",
    "web.styles",
    "web.blocks",
    "web.notifications",
    "web.site_tests",
    "django_hosts",
    "web.domens",
    "qr_code",
    "sass_processor",
    "daphne",
    "channels",
    "rest_framework",
    "web.emails",
    "corsheaders",
    "web.materials",
    "web.system",
    "django_user_agents",
]


ASGI_APPLICATION = "web.core.asgi.application"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis", 6379)],
            # "hosts": [("localhost", 6379), ("bankomag.ru", 6379), ("idri.ru", 6379)],
        },
    },
}

AUTH_USER_MODEL = "user.User"

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django_user_agents.middleware.UserAgentMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "web.site_statistics.raw_session_middleware.RawSessionMiddleware",
    "web.site_statistics.user_activity_middleware.UserActivityMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django_hosts.middleware.HostsRequestMiddleware",
    "django_hosts.middleware.HostsResponseMiddleware",
    "web.user.middleware.JwtAuthMiddleware",
    "web.admin.middleware.AdminMiddleware",
    "web.site_tests.middleware.ExceptionLoggingMiddleware",
]

ROOT_URLCONF = "web.core.urls"

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

WSGI_APPLICATION = "web.core.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR.parent.parent / "db.sqlite3",
        "OPTIONS": {
            "timeout": 100,
        },
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# LANGUAGE_CODE = "en-us"

TIME_ZONE = "Europe/Moscow"

USE_TZ = True
USE_I18N = True


# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "media")
STATICFILES_DIR = os.path.join(BASE_DIR, "static")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR.parent.parent, "static")


# email settings

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True

EMAIL_HOST_USER = str(os.getenv("EMAIL_HOST_USER"))
EMAIL_HOST_PASSWORD = str(os.getenv("EMAIL_HOST_PASSWORD"))

SERVER_EMAIL = EMAIL_HOST_USER
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587

# celery

CELERY_BROKER_URL = str(os.getenv("CELERY_BROKER_URL"))

# domains

ROOT_HOSTCONF = "web.core.hosts"
DEFAULT_HOST = "www"

DATA_UPLOAD_MAX_MEMORY_SIZE = 20_971_520
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SESSION_COOKIE_SECURE = False

CORS_ORIGIN_ALLOW_ALL = True

AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]

SASS_ROOT = os.path.join(BASE_DIR, "static", "scss")
SASS_PROCESSOR_ROOT = SASS_ROOT

COMPRESS_PRECOMPILERS = (("text/x-scss", "django_libsass.SassCompiler"),)

STATICFILES_DIRS = (os.path.join(BASE_DIR, "static"),)

SASS_PROCESSOR_INCLUDE_DIRS = (os.path.join(BASE_DIR, "static"), SASS_ROOT)

STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
    "sass_processor.finders.CssFinder",
)

SASS_PROCESSOR_ENABLED = True

FILE_UPLOAD_MAX_MEMORY_SIZE = 3 * 1024 * 1024  # (3MEGABYTES)
DATA_UPLOAD_MAX_MEMORY_SIZE = FILE_UPLOAD_MAX_MEMORY_SIZE


CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "Custom",
        "toolbar_Custom": [
            ["Styles", "Format"],
            ["Bold", "Italic", "Underline", "Strike", "Undo", "Redo"],
            ["NumberedList", "BulletedList"],
            ["Link", "Unlink", "Anchor"],
            ["Image", "Table", "HorizontalRule"],
            ["JustifyLeft", "JustifyCenter", "JustifyRight"],
            ["TextColor"],
            ["Smiley"],
            ["Source"],
        ],
    },
}

APPEND_SLASH = True

SYSTEM_EMAIL_HOST_USER = "system@bmdom.ru"

CSRF_TRUSTED_ORIGINS = [
    "https://bmdom.ru",
    "https://bankomag.ru",
    "https://idri.ru",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]


CORS_ALLOWED_ORIGINS = [
    "https://bmdom.ru",
    "https://bankomag.ru",
    "https://idri.ru",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

CORS_ORIGIN_WHITELIST = [
    "https://bmdom.ru",
    "https://bankomag.ru",
    "https://idri.ru",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = "*"

SESSION_COOKIE_AGE = 60 * int(os.getenv("SESSION_EXPIRES_IN"))

USE_TZ = False

USER_ACTIVITY_SESSION_KEY = os.getenv("USER_ACTIVITY_SESSION_KEY")
RAW_SESSION_SESSION_KEY = os.getenv("RAW_SESSION_SESSION_KEY")

SESSION_SAVE_EVERY_REQUEST = True
