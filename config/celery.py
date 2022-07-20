import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery ('config')
app.config_from_object('django.conf:settings', namespace ='CELERY')
app.autodiscover_tasks()
CELERY_BEAT_SCHEDULE = {
    'update_table': {
        'task': 'google_sheets_service.tasks.update_table_task',
        'schedule': crontab(minute='*/1'),
    },
}

if __name__ == '__main__':
    app.start()