from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import transaction

from jobdetails.models import JobInfo, JobData
from .utils import write_to_storage, strip_data, tld_check, page_get_html, convert_to_b64


@csrf_exempt
def api_crawler_agent_post(request):
    if request.method == 'POST':
        crawler_id = request.POST.get("crawler_id", 1)
        tld = request.POST.get("tld", "")
        page_url_trimmed = request.POST.get("page_trimmed", "")
        page_url = request.POST.get("page", "")
        xpath_list = [
                request.POST.get("title_xpath", ""),
                request.POST.get("location_xpath", ""),
                request.POST.get("nature_xpath", ""),
                request.POST.get("desc_xpath", "")
                ]
        try:
            job = JobInfo.objects.filter(crawler_agent_id=crawler_id, job_page_url__startswith=str(page_url_trimmed.encode('utf-8')))
        except:
            pass
        if job:
            return HttpResponse("Page previously crawled")
        else:
            response = page_get_html(page_url)
            if response is 0:
                job_false_pagehit = JobInfo.objects.create(
                        crawler_agent_id=int(crawler_id.encode('utf-8')),
                        job_page_url=str(page_url.encode('utf-8')),
                        job_title='Domain could not be hit',
                        path_gcs='',
                        status=False
                        )
                return HttpResponse("Domain could not be hit")
            else:
                check = tld_check(tld.encode('utf-8'), response['url'].encode('utf-8'))
                if check == "False":
                    job_false_tld = JobInfo.objects.create(
                            crawler_agent_id=int(crawler_id.encode('utf-8')),
                            job_page_url=str(page_url.encode('utf-8')),
                            job_title='TLD Failed',
                            path_gcs='',
                            status=False
                            )
                    return HttpResponse("Page not in TLD Domain")
                else:
                    title = str(response['title']).encode('utf-8')
                    job_html_b64 = convert_to_b64(response['text'])
                    params = {
                        'crawler_id': crawler_id,
                        'tld': tld,
                        'job_page_url': page_url,
                        'job_title': title,
                        'job_html_b64': job_html_b64,
                        }
                    status = write_to_storage(**params)
                    stripped_data_list = strip_data(xpath_list, response['text'])
                    if status['status'] == 'Wrote to gcloud storage' and stripped_data_list is not 0:
                        with transaction.atomic():
                            job = JobInfo.objects.create(
                                crawler_agent_id=int(crawler_id.encode('utf-8')),
                                job_page_url=str(page_url.encode('utf-8')),
                                job_title=str(title.encode('utf-8')),
                                path_gcs=str(status['path']),
                                status=True
                                )
                            job.save()
                            job = JobInfo.objects.get(id=int(job.id))
                            job_data = JobData.objects.create(
                                title=stripped_data_list[0],
                                location=stripped_data_list[1],
                                nature=stripped_data_list[2],
                                desc=stripped_data_list[3],
                                job=job,
                                )
                        return JsonResponse({'status': 'Wrote to Gcloud & Extarcted Data', 'job': job.id})
                    else:
                        job_false_data = JobInfo.objects.create(
                                crawler_agent_id=int(crawler_id.encode('utf-8')),
                                job_page_url=str(page_url.encode('utf-8')),
                                job_title='Data Extraction Failed',
                                path_gcs='',
                                status=False
                                )

                        return JsonResponse({'status': 'Could not write to Gcloud/ Extract Data', 'job': "null"})
    else:
        return HttpResponse("<p>Are you sure you are posting data?</p>")
