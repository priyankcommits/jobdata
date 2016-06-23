# celery tasks to schedule

from __future__ import absolute_import
from jobdata import celery_app
from celery import shared_task, task

@shared_task
def add(x,y):
    return x+y
