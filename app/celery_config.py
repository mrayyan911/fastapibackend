from celery import Celery
import os
# Initialize Celery with Redis as broker and backend
celery_obj = Celery(
    'worker',
    broker=os.getenv('REDIS_URL'),
    backend=os.getenv('REDIS_URL'),
)