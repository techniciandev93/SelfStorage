import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'selfstorage.settings')
app = Celery('selfstorage')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'user_notification_everyday': {
        'task': 'users.tasks.send_notifications',
        'schedule': crontab(minute='0', hour='0'),
        # 'for test use this
        # 'schedule': crontab(minute='*'),
    }
}
