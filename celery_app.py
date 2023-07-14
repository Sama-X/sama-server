"""
Celery app
"""
import os
import sys

from celery import Celery
from celery.schedules import crontab

from base.config import get_settings


sys.path.append(os.path.join('./apps'))
settings = get_settings()

celery_app = Celery(
    "sama-server", broker=settings.celery_broker_url, backend=settings.celery_result_backend
)
celery_app.autodiscover_tasks(['sama.tasks'])
celery_app.conf.update(
    enable_utc=True,
    timezone='Asia/Shanghai'
)
celery_app.conf.beat_schedule = {
    'get_sama_nodes_task': {
        'task': 'sama.tasks.get_sama_nodes',
        'schedule': crontab(minute='*/1'),
    }
}
