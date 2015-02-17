from __future__ import absolute_import

import os

from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SocialLearning.config')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Local')

from configurations import importer
importer.install()

app = Celery('sociallearning')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
