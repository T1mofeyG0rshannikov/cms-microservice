import os

from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.core.settings")
app = Celery("core", broker=settings.CELERY_BROKER_URL, backend=settings.CELERY_BROKER_URL)
app.config_from_object(settings, namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'add-every-30-seconds': {
        'task': 'infrastructure.logging.tasks.detect_single_page_sessions',
        'schedule': 30.0,
    },
}

app.conf.update(
    timezone='Europe/Moscow', 
    enable_utc=True, # Храним время в UTC
    worker_hijack_root_logger=False, # Переопределяем настройки логгирования
)