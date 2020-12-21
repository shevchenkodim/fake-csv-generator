from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'FakeCSV.settings')

app = Celery('FakeCSV')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.update(
     enable_utc=True,
     timezone='Europe/Kiev',
)
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
app.conf.update(BROKER_URL=os.environ['REDISTOGO_URL:'],
                CELERY_RESULT_BACKEND=os.environ['REDISTOGO_URL:'])
