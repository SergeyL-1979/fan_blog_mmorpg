import os
from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bulletin.settings')

app = Celery('NewsPaper')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'action_every_monday_8am': {
        'task': 'mmorpg.tasks.week_email_sending',
        'schedule': crontab(hour='8', minute='0', day_of_week='mon'),  # crontab(hour=0, minute=10, day_of_week=5),
    },
}
