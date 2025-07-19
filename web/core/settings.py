# import logging
import os

# import sys
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
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "adminsortable2",
    "colorfield",
    "ckeditor",
    "web.blocks",
    "web.catalog",
    "web.common",
    "web.settings",
    "web.styles",
    "rest_framework",
    "corsheaders",
    "debug_toolbar",
]


ASGI_APPLICATION = "web.core.asgi.application"


MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django_user_agents.middleware.UserAgentMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

INTERNAL_IPS = [
    "127.0.0.1",
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
        "ENGINE": "django.db.backends.mysql",  # <-- UPDATED line
        "NAME": "bankomag_cms",  # <-- UPDATED line
        "USER": "root",  # <-- UPDATED line
        "PASSWORD": "root",  # <-- UPDATED line
        "HOST": "localhost",  # <-- UPDATED line
        "PORT": "3306",
        "OPTIONS": {
            "charset": "utf8mb4",
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
    "compressor.finders.CompressorFinder",
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
        "allowedContent": True,
    },
}

APPEND_SLASH = True

SYSTEM_EMAIL_HOST_USER = "system@bmdom.ru"

CSRF_TRUSTED_ORIGINS = [
    "https://bmdom.ru",
    "https://*.bankomag.ru",
    "https://bankomag.ru",
    "https://idri.ru",
    "https://*.idri.ru",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]


CORS_ALLOWED_ORIGINS = [
    "https://bmdom.ru",
    "https://*.bankomag.ru",
    "https://bankomag.ru",
    "https://idri.ru",
    "https://*.idri.ru",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://localhost",
]

CORS_ORIGIN_WHITELIST = [
    "https://bmdom.ru",
    "https://*.bankomag.ru",
    "https://bankomag.ru",
    "https://idri.ru",
    "https://*.idri.ru",
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "http://127.0.0.1",
    "http://localhost",
]
CORS_ALLOW_CREDENTIALS = True

SESSION_COOKIE_AGE = 60 * int(os.getenv("EXPIRES_IN"))  # type: ignore

USE_TZ = False

USER_ACTIVITY_SESSION_KEY = os.getenv("USER_ACTIVITY_SESSION_KEY")
RAW_SESSION_SESSION_KEY = os.getenv("RAW_SESSION_SESSION_KEY")

SESSION_SAVE_EVERY_REQUEST = True

USER_ACTIVITY_COOKIE_NAME = "user_activity"
RAW_SESSION_COOKIE_NAME = "raw_session"
SEARCHER_COOKIE_NAME = "searcher_session"


CORS_ALLOW_HEADERS = ("content-disposition", "accept-encoding", "content-type", "accept", "origin", "authorization")
"""
LOGGING = {
    "version": 1,
    "disabled_existing_loggers": False,
    "formatters": {
        "main_format": {
            "format": "{asctime} - {levelname} - {module} - {filename} - {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "main_format",
        },
        "file": {
            "class": "logging.FileHandler",
            "formatter": "main_format",
            "filename": "information.log",
        },
    },
    "loggers": {
        "main": {
            "handlers": ["console", "file"],
            "level": "INFO",
            "propagate": True,
        },
        #'django.db.backends': {
        #    'level': 'DEBUG',
        #    'handlers': ['console'],
        #}
    },
}


logger = logging.getLogger("main")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
"""

CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": os.path.join(BASE_DIR, "bankomag_cache"),
    }
}


MIGRATION_MODULES = {
    "user": "infrastructure.persistence.migrations.user",
    "blocks": "infrastructure.persistence.migrations.blocks",
    "site_statistics": "infrastructure.persistence.migrations.site_statistics",
    "catalog": "infrastructure.persistence.migrations.catalog",
    "account": "infrastructure.persistence.migrations.account",
    "settings": "infrastructure.persistence.migrations.settings",
    "styles": "infrastructure.persistence.migrations.styles",
    "notifications": "infrastructure.persistence.migrations.notifications",
    "site_tests": "infrastructure.persistence.migrations.site_tests",
    "materials": "infrastructure.persistence.migrations.materials",
    "system": "infrastructure.persistence.migrations.system",
    "messanger": "infrastructure.persistence.migrations.messanger",
}


REST_FRAMEWORK = {"EXCEPTION_HANDLER": "web.site_tests.exc_handler.my_exception_handler"}


COMPRESS_ENABLED = True
# COMPRESS_OFFLINE = True
COMPRESS_CSS_HASHING_METHOD = "hash"
