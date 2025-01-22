from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media_admin.settings')

app = Celery('social_media_admin')

# Use a string here to avoid serializing the configuration object to child processes.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Discover task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

# Define the beat schedule for periodic tasks
app.conf.beat_schedule = {
    # Run the bulk_schedule_posts task every minute
    'process_scheduled_posts': {
        'task': 'content_management.tasks.bulk_schedule_posts',
        'schedule': crontab(minute='*'),  # Every minute
    },
}
