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
from crawler.views import crawler_agent_post, crawler_agent_check, job_details_agents, job_details_dates, job_details_files, job_details_view_html, job_details_view_json

urlpatterns = [
    url(r'^$', job_details_agents, name='job_details_agents'),
    url(r'^(?P<crawler>[0-9]+)/dates/$', job_details_dates, name='job_details_dates'),
    url(r'^(?P<crawler>[0-9]+)/date/(?P<date>[-\w]+)/files/$', job_details_files, name='job_details_files'),
    url(r'^(?P<file>.*)/view_html/$', job_details_view_html, name='job_details_view_html'),
    url(r'^(?P<file>.*)/view_json/$', job_details_view_json, name='job_details_view_json'),
    url(r'^crawler_agent_post/$', crawler_agent_post, name='crawler_agent_post'),
    url(r'^crawler_agent_check/$', crawler_agent_check, name='crawler_agent_check'),
]
