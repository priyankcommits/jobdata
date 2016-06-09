from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .utils import write_to_gcloud_storage, write_to_local_storage


@csrf_exempt
def crawler_agent_post(request):
    if request.method == 'POST':
        id = request.POST.get("id", 1)
        tld = request.POST.get("tld", "dice.com")
        job_url = request.POST.get("url", "")
        job_html_b64 = request.POST.get("job_html_b64", "")
        status = write_to_local_storage(id, tld, job_url, job_html_b64)

        return HttpResponse(status)
    else:
        return HttpResponse("<p>Are you sure you are posting data?</p>")
