from celery import Celery, states

app = Celery(
    'tasks',
    broker='pyamqp://guest@localhost//',
    result_serializer='json',
)

app.conf.update(
    database_engine_options={'echo': True},
    timezone='America/Sao_Paulo',
)

from glpi.task import task_glpi_create
from sso.task import task_sso_create
from notification.task import task_notification_group, task_notification