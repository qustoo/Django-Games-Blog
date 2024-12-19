import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "games_blog.settings")

app = Celery(
    "publish",
    broker_connection_retry=False,
    broker_connection_retry_on_startup=True,
)

broker_connection_retry = False

# Загружаем конфигурацию из файла настроек Django
app.config_from_object("django.conf:settings", namespace="CELERY")
# Обнаруживаем задачи в приложениях Django
app.autodiscover_tasks()
