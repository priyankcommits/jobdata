from __future__ import unicode_literals

from django.db import models


class CrawlerAgent(models.Model):
    tld = models.CharField(max_length=100)
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.tld

    def __unicode__(self):
        return u"%s" % self.id


class JobInfo(models.Model):
    crawler_agent = models.ForeignKey(CrawlerAgent)
    job_url = models.CharField(max_length=500)
    path_gcs = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return u"%s" % self.crawler_agent_id
