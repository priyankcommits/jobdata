import base64
from time import sleep
import requests
from BeautifulSoup import BeautifulSoup

import os
api_host = os.getenv('API_HOST', 'localhost:8001')


class BaseCrawler(object):

    def post_to_data_extract(
            self, title_xpath, location_xpath, nature_xpath, desc_xpath,
            page, job
            ):
        endpoint = "{0}/crawler_agent_data/".format(api_host)
        r = requests.post(
            endpoint,
            data={
                'title_xpath': title_xpath,
                'location_xpath': location_xpath,
                'nature_xpath': nature_xpath,
                'desc_xpath': desc_xpath,
                'page': page,
                'job': job
            }
        )

        return str(r.text.encode('utf-8'))

    def post_to_jobdata(self, title, page_new, html_text, crawler_id, tld):
        endpoint = "{0}/crawler_agent_post/".format(api_host)
        if html_text and html_text != 'None':
            job_html_b64 = base64.b64encode(html_text)
            r = requests.post(
                endpoint,
                data={
                    'crawler_id': crawler_id,
                    'tld': tld,
                    'job_page_url': page_new,
                    'job_title': title,
                    'job_html_b64': job_html_b64
                }
            )
            return r.status_code, r.reason, r.text
        else:
            return "Html has nothing"

    def page_get_html(self, page_new):
        try:
            r = requests.get(page_new)
            if r.status_code == 200:
                page_new_request = requests.get(page_new)
                soup_page_new = BeautifulSoup(page_new_request.text)
                title = soup_page_new.findAll('title')
                # html_text = str(r.text.encode('utf-8'))
                # sleep(10)
                return {'r': r, 'title': title}
        except Exception as e:
            print 'error', e
            return 0

    def get_title(self,html):
        soup = BeautifulSoup(html)
        title = soup.findAll('title')

        return {'title': title}

    def tld_check(self, page, tld):
        if tld in page[:30]:
            return "True"
        else:
            return "False"
