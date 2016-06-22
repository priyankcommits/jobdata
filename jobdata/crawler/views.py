from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from datetime import datetime
from sets import Set
import base64
import json
from collections import OrderedDict

from .models import CrawlerAgent, JobInfo
from .utils import write_to_storage
from gcloud_storage import GcloudStorage


@csrf_exempt
def crawler_agent_check(request):
    if request.method == 'POST':
        crawler_id = request.POST.get("crawler_id", 1)
        job_page_url = request.POST.get("job_page_url", "")
        try:
            job = JobInfo.objects.filter(crawler_agent_id=crawler_id, job_page_url=job_page_url)
        except Exception as e:
            return HttpResponse(e)
        if job:
            return HttpResponse("False")
        else:
            return HttpResponse("True")
    else:
        return HttpResponse("<p>Are you posting data?</p>")


@csrf_exempt
def crawler_agent_post(request):
    if request.method == 'POST':
        crawler_id = request.POST.get("crawler_id", 1)
        tld = request.POST.get("tld", "dice.com")
        job_page_url = request.POST.get("job_page_url", "")
        job_title = request.POST.get("job_title", "")
        job_html_b64 = request.POST.get("job_html_b64", "")
        try:
            crawler_agent = CrawlerAgent.objects.get(id=crawler_id, tld=tld)
        except Exception as e:
            return HttpResponse(e)
        if crawler_agent:
            params = {
                    'crawler_id': crawler_id,
                    'tld': tld,
                    'job_page_url': job_page_url,
                    'job_title': job_title,
                    'job_html_b64': job_html_b64,
                    }
            status = write_to_storage(**params)
            if status['status'] == 'Wrote to gcloud storage':
                job = JobInfo.objects.create(
                    crawler_agent_id=int(crawler_id),
                    job_page_url=str(job_page_url),
                    job_title=str(job_title),
                    path_gcs=str(status['path'])
                    )
            return HttpResponse(status['status'])
    else:
        return HttpResponse("<p>Are you sure you are posting data?</p>")


def job_details_agents(request):
    if request.method == 'GET':
        crawler_agents = CrawlerAgent.objects.all()
        for crawler in crawler_agents:
            crawler.votes = JobInfo.objects.filter(crawler_agent_id=crawler.id).count()
        return render(request, 'crawler/agents.html', {'crawlers': crawler_agents, })
    else:
        return HttpResponse("<p>There is no posting here :)</p>")


def job_details_dates(request, crawler):
    if request.method == 'GET':
        crawler_id = crawler
        jobs = JobInfo.objects.filter(crawler_agent_id=int(crawler_id)).order_by('-created_at')
        dates_dict = {}
        for job in jobs:
            if str(job.created_at.date()) in dates_dict:
                dates_dict[str(job.created_at.date())] = int(dates_dict[str(job.created_at.date())]) + 1
            else:
                dates_dict[str(job.created_at.date())] = 1
            ordered_dates_dict = OrderedDict(sorted(dates_dict.items()))

    return render(request, 'crawler/dates.html', {'counts': ordered_dates_dict, 'crawler_id': crawler_id})


def job_details_files(request, crawler, date):
    if request.method == 'GET':
        crawler_id = crawler
        date = date
        date_field = datetime.strptime(str(date), '%Y-%m-%d')
        files = JobInfo.objects.filter(crawler_agent_id=int(crawler_id), created_at__startswith=str(date_field.date())).order_by('-created_at')

        return render(request, 'crawler/files.html', {'files': files, 'date': date, 'crawler_id_date': crawler_id})


def job_details_view_json(request, crawler, date, file):
    if request.method == 'GET':
        crawler_id_date_file = crawler
        date = date
        file = file
        gcs = GcloudStorage()
        bucket = gcs.get_bucket('job-data-development')
        blob = bucket.get_blob(str(file))
        blob_string = blob.download_as_string()

        return render(request, 'crawler/view_json.html', {'title': file, 'blob_string': blob_string, 'date': date, 'crawler_id_date_file': crawler_id_date_file})


def job_details_view_html(request, crawler, date, file):
    if request.method == 'GET':
        crawler_id_date_file = crawler
        date = date
        file = file
        gcs = GcloudStorage()
        bucket = gcs.get_bucket('job-data-development')
        blob = bucket.get_blob(str(file))
        blob_string = blob.download_as_string()
        blob_json = json.loads(str(blob_string))
        html_b64 = str(blob_json['job_html_b64'])
        html = base64.b64decode(html_b64)
        title = str(blob_json['job_title'])

        return render(request, 'crawler/view_html.html', {'html': html, 'title': title, 'date': date, 'crawler_id_date_file': crawler_id_date_file})
