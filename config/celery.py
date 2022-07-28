import logging
import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

logging.basicConfig(
        level=logging.DEBUG,
        filename='program.log',
        filemode='w',
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s',
    )

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

if __name__ == '__main__':
    app.start()
