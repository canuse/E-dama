# Create your models here.
import datetime

from django.db import models


class MahjongRecord(models.Model):
    """
    record query table
    """
    log_url = models.URLField(blank=True)
    player_name = models.CharField(max_length=16)
    creat_date = models.DateTimeField(default=datetime.datetime.now)

class Queue(models.Model):
    """
    Choose this low efficiency way due to these reasons:
    1. Queue can be edited through django admin
    2. Celery doesn't work properly on win10
    """
    log_url = models.URLField(blank=True)
    player_name = models.CharField(max_length=16)
    creat_date = models.DateTimeField(default=datetime.datetime.now)
    priority = models.IntegerField(default=10)