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
    is_finished = models.BooleanField(default=False)
