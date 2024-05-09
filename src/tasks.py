from celery import Celery

app = Celery(
    'tasks',
    broker='pyamqp://guest@localhost//',
    result_serializer='json',
)

app.conf.update(
    timezone='America/Sao_Paulo',
)

from glpi.task import task_glpi_create
from notification.task import task_notification_wpp