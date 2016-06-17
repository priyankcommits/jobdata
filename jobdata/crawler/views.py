from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from datetime import datetime
from sets import Set
import base64
import json

from .models import CrawlerAgent, JobInfo
from .utils import write_to_storage
from gcloud_storage import GcloudStorage


@csrf_exempt
def crawler_agent_post(request):
    if request.method == 'POST':
        crawler_id = request.POST.get("crawler_id", 1)
        tld = request.POST.get("tld", "dice.com")
        job_url = request.POST.get("job_url", "")
        job_html_b64 = request.POST.get("job_html_b64", "")
        try:
            crawler_agent = CrawlerAgent.objects.get(id=crawler_id, tld=tld)
        except Exception as e:
            return HttpResponse(e)
        if crawler_agent:
            params = {
                    'crawler_id': crawler_id,
                    'tld': tld,
                    'job_url': job_url,
                    'job_html_b64': job_html_b64,
                    }
            status = write_to_storage(**params)
            if status['status'] == 'Wrote to gcloud storage':
                job = JobInfo.objects.create(
                    crawler_agent_id=int(crawler_id),
                    job_url=str(job_url),
                    path_gcs=str(status['path'])
                    )
            return HttpResponse(status['status'])
    else:
        return HttpResponse("<p>Are you sure you are posting data?</p>")


def job_details_folders(request):
    if request.method == 'GET':
        crawler_agents = CrawlerAgent.objects.all()
        return render(request, 'crawler/agents.html', {'crawlers': crawler_agents, })
    else:
        return HttpResponse("<p>There is no posting here :)</p>")


def job_details_dates(request):
    if request.method == 'GET':
        crawler_id = request.GET.get("id", 1)
        dates = JobInfo.objects.filter(crawler_agent_id=int(crawler_id))
        date_folders_list = []
        try:
            for date in dates:
                date_folders = date.created_at.date()
                date_folders_list.append(date_folders)
            date_folders_list_str = []
            for date in date_folders_list:
                date_folders_list_str.append(str(date))
            date_set = Set(date_folders_list_str)
            return render(request, 'crawler/dates.html', {'dates': date_set, 'crawler_id': crawler_id})
        except Exception as e:
            return HttpResponse(e)


def job_details_files(request):
    if request.method == 'GET':
        crawler_id = request.GET.get("id", 1)
        date = request.GET.get("date", "2016-06-13")
        date_field = datetime.strptime(str(date), '%Y-%m-%d')
        files = JobInfo.objects.filter(crawler_agent_id=int(crawler_id), created_at__startswith=str(date_field.date()))
        return render(request, 'crawler/files.html', {'files': files})


def job_details_view_html(request):
    if request.method == 'GET':
        file = request.GET.get("file","")
        gcs = GcloudStorage()
        bucket = gcs.get_bucket('job-data-development')
        blob = bucket.get_blob(str(file))
        blob_string = blob.download_as_string()
        blob_json = json.loads(str(blob_string))
        html_b64 = str(blob_json['job_html_b64'])
        html = base64.b64decode(html_b64)

        return HttpResponse(html)
