"""jobdata URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from crawler.views import crawler_agent_post, job_details_folders, job_details_dates, job_details_files, job_details_view_html

urlpatterns = [
    url(r'^$', job_details_folders, name='job_details_folders'),
    url(r'^dates/$', job_details_dates, name='job_details_dates'),
    url(r'^files/$', job_details_files, name='job_details_files'),
    url(r'^view/$', job_details_view_html, name='job_details_view_html'),
    url(r'^crawler_agent_post/$', crawler_agent_post, name='crawler_agent_post'),
    url(r'^admin/', admin.site.urls),
]
