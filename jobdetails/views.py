from django.http import HttpResponse
from django.shortcuts import render
from datetime import datetime
import base64
import json
from collections import OrderedDict

from .models import CrawlerAgent, JobInfo, JobData
from gcloud_storage import GcloudStorage


def job_details_agents(request):
    if request.method == 'GET':
        crawler_agents = CrawlerAgent.objects.all()
        for crawler in crawler_agents:
            crawler.votes = JobInfo.objects.filter(crawler_agent_id=crawler.id, status=True).count()
        return render(request, 'jobdetails/agents.html', {'crawlers': crawler_agents, })
    else:
        return HttpResponse("<p>There is no posting here :)</p>")


def job_details_dates(request, crawler):
    if request.method == 'GET':
        crawler_id = crawler
        crawler = CrawlerAgent.objects.get(id=int(crawler_id.encode('utf-8')))
        jobs = JobInfo.objects.filter(crawler_agent_id=int(crawler.id), status=True).order_by('-created_at')
        dates_dict = {}
        for job in jobs:
            if str(job.created_at.date()) in dates_dict:
                dates_dict[str(job.created_at.date())] = int(dates_dict[str(job.created_at.date())]) + 1
            else:
                dates_dict[str(job.created_at.date())] = 1
            ordered_dates_dict = OrderedDict(sorted(dates_dict.items()))
        title_list = []
        location_list = []
        nature_list = []
        desc_list = []
        jobs = JobData.objects.all()
        for date_key in ordered_dates_dict.keys():
            title_length = 0
            location_length = 0
            nature_length = 0
            desc_length = 0
            title_count = 0
            location_count = 0
            nature_count = 0
            desc_count = 0
            for job in jobs:
                if str(job.job.created_at.date()) == str(date_key):
                    title_length += len(str(job.title))
                    title_count += 1
            title_list.append(title_length/title_count)
            for job in jobs:
                if str(job.job.created_at.date()) == str(date_key):
                    location_length += len(str(job.location))
                    location_count += 1
            location_list.append(location_length/location_count)
            for job in jobs:
                if str(job.job.created_at.date()) == str(date_key):
                    nature_length += len(str(job.nature))
                    nature_count += 1
            nature_list.append(nature_length/nature_count)
            for job in jobs:
                if str(job.job.created_at.date()) == str(date_key):
                    desc_length += len(str(job.desc))
                    desc_count += 1
            desc_list.append(desc_length/desc_count)

    return render(request, 'jobdetails/dates.html', {'title_list': title_list, 'location_list': location_list, 'nature_list': nature_list, 'desc_list': desc_list, 'counts': ordered_dates_dict, 'crawler_id': crawler})


def job_details_files(request, crawler, date):
    if request.method == 'GET':
        crawler_id = crawler
        crawler = CrawlerAgent.objects.get(id=int(crawler_id.encode('utf-8')))
        date = date
        date_field = datetime.strptime(str(date), '%Y-%m-%d')
        files = JobInfo.objects.filter(crawler_agent_id=int(crawler.id), status=True, created_at__startswith=str(date_field.date())).order_by('-created_at')

        return render(request, 'jobdetails/files.html', {'files': files, 'date': date, 'crawler_id_date': crawler})


def job_details_view_json(request, crawler, date, file):
    if request.method == 'GET':
        crawler_id = crawler
        crawler = CrawlerAgent.objects.get(id=int(crawler_id.encode('utf-8')))
        date = date
        file = file
        gcs = GcloudStorage()
        bucket = gcs.get_bucket('job-data-development')
        blob = bucket.get_blob(str(file))
        blob_string = blob.download_as_string()

        return render(request, 'jobdetails/view_json.html', {'title': file, 'blob_string': blob_string, 'date': date, 'crawler_id_date_file': crawler})


def job_details_view_html(request, crawler, date, file):
    if request.method == 'GET':
        crawler_id = crawler
        crawler = CrawlerAgent.objects.get(id=int(crawler_id.encode('utf-8')))
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

        return render(request, 'jobdetails/view_html.html', {'html': html, 'title': title, 'date': date, 'crawler_id_date_file': crawler})


def job_details_view_data(request, crawler, date, job):
    if request.method == 'GET':
        crawler_id = crawler
        crawler = CrawlerAgent.objects.get(id=int(crawler_id.encode('utf-8')))
        date = date
        job_data = JobData.objects.get(job_id=int(job))
        title = job_data.title
        return render(request, 'jobdetails/view_data.html', {'title': title, 'job_data': job_data, 'date': date, 'crawler_id_date_file': crawler})
