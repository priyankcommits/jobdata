from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from .models import CrawlerAgent
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
            return HttpResponse(status['status'])
    else:
        return HttpResponse("<p>Are you sure you are posting data?</p>")


def job_details(request):
    if request.method == 'GET':
        gcs = GcloudStorage()
        gcs_objects = gcs.list_objects()
        print gcs_objects
        list_objects = list(gcs_objects)
        print list_objects
        return render(request, 'crawler/details.html', {'list': list_objects, })
