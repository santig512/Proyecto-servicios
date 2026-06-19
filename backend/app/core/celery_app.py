from celery import Celery
from app.core.config import settings

celery = Celery(
    'worker',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

celery.conf.task_routes = {
    'app.notifications.tasks.*': {'queue': 'notifications'},
}

celery.conf.worker_prefetch_multiplier = 1
celery.conf.task_acks_late = True
