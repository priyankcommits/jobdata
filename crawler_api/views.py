from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from jobdetails.models import CrawlerAgent, JobInfo, JobData
from .utils import write_to_storage, strip_data


@csrf_exempt
def crawler_agent_check(request):
    if request.method == 'POST':
        crawler_id = request.POST.get("crawler_id", 1)
        job_page_url = request.POST.get("job_page_url", "")
        try:
            job = JobInfo.objects.filter(crawler_agent_id=crawler_id, job_page_url=job_page_url)
        except Exception as e:
            return HttpResponse(str(e))
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
            return HttpResponse(str(e))
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
                    crawler_agent_id=int(crawler_id.encode('utf-8')),
                    job_page_url=str(job_page_url.encode('utf-8')),
                    job_title=str(job_title.encode('utf-8')),
                    path_gcs=str(status['path'])
                    )
                job.save()
                return JsonResponse({'status': status['status'], 'job': job.id})
            else:
                return JsonResponse({'status': 'Could not write to Gcloud', 'job': 1})
    else:
        return HttpResponse("<p>Are you sure you are posting data?</p>")


@csrf_exempt
def crawler_agent_data(request):
    if request.method == 'POST':
        job_id = request.POST.get("job", 1)
        job = JobInfo.objects.get(id=int(job_id))
        page = request.POST.get("page", "")
        unstripped_data_list = [request.POST.get("title_xpath", ""),
                request.POST.get("location_xpath", ""),
                request.POST.get("nature_xpath", ""),
                request.POST.get("desc_xpath", "")]
        stripped_data_list = strip_data(unstripped_data_list, page)
        if stripped_data_list is not 0:
            job_data = JobData.objects.create(
                    title=stripped_data_list[0],
                    location=stripped_data_list[1],
                    nature=stripped_data_list[2],
                    desc=stripped_data_list[3],
                    job=job,
                    )
            return HttpResponse("Wrote Data Extracted to DB")
        else:
            return HttpResponse("Could not write Extracted Data to DB")
    else:
        return HttpResponse("<p>Are you sure you are posting data?</p>")


