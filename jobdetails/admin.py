from django.contrib import admin
from .models import CrawlerAgent, JobInfo, JobData


# Register your models here.
class CrawlerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'tld')


class JobInfoAdmin(admin.ModelAdmin):
    list_display = ('id', 'job_title', 'crawler_agent_id', 'path_gcs', 'job_page_url', 'created_at')


class JobDataAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'location', 'nature', 'desc', 'job')


admin.site.register(CrawlerAgent, CrawlerAdmin)
admin.site.register(JobInfo, JobInfoAdmin)
admin.site.register(JobData, JobDataAdmin)
