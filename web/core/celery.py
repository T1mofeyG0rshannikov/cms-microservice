import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.core.settings")
app = Celery("core", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_BROKER_URL)
app.config_from_object(settings, namespace="CELERY")
app.autodiscover_tasks()
