from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'olx_rem.settings')

app = Celery('olx_rem',
             backend='redis://localhost',
             broker='redis://localhost')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# celery -A classified_ads worker --loglevel=info
