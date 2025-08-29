from celery import shared_task
from django.db.models import F

from .models import Content


@shared_task
def increment_counter(content_id):
    Content.objects.filter(id=content_id).update(counter=F('counter') + 1)