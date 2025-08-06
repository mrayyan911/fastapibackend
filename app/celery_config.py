from celery import Celery
import os
# Initialize Celery with Redis as broker and backend
celery_obj = Celery(
    'app',
    broker=os.getenv('REDIS_URL'),
    backend=os.getenv('REDIS_URL'),
    include=['app.celery_tasks.send_verification_email']
)
