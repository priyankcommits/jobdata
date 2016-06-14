from django.contrib import admin
from .models import CrawlerAgent


# Register your models here.
class CrawlerAdmin(admin.ModelAdmin):
    list_display = CrawlerAgent._meta.get_all_field_names()

admin.site.register(CrawlerAgent, CrawlerAdmin)
