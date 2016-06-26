import base64
from time import sleep
import requests


class BaseCrawler(object):

    def post_to_data_extract(self, title_xpath, location_xpath, nature_xpath, desc_xpath, page, job):
        r = requests.post("http://localhost:8001/crawler_agent_data/",
                data={'title_xpath': title_xpath,
                    'location_xpath': location_xpath,
                    'nature_xpath': nature_xpath,
                    'desc_xpath': desc_xpath,
                    'page': page,
                    'job': job})

        return str(r.text.encode('utf-8'))

    def post_to_jobdata(self, title, page_new, html_text, crawler_id, tld):
        if html_text and html_text != 'None':
            job_html_b64 = base64.b64encode(html_text)
            r = requests.post("http://localhost:8001/crawler_agent_post/",
                    data={'crawler_id': crawler_id,
                        'tld': tld,
                        'job_page_url': page_new,
                        'job_title': title,
                        'job_html_b64': job_html_b64})
            return r.status_code, r.reason, r.text
        else:
            return "Html has nothing"

    def page_get_html(self, title, page_new, crawler_id, tld):
        try:
            r = requests.get(page_new)
            if r.status_code == 200:
                # html_text = str(r.text.encode('utf-8'))
                sleep(10)
                return r
        except Exception as e:
            print 'error', e
            pass
        else:
            pass

    def tld_check(self, page, tld):
        if tld in page[:20]:
            return "True"
        else:
            return "False"
