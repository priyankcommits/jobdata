from __future__ import unicode_literals

from django.utils import timezone
from django.db import models

class CrawlerAgent(models.Model):
    tld =models.CharField(max_length = 100)
    name = models.CharField(max_length = 300)

    def __str__(self):
        return self.tld
