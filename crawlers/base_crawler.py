import base64
from time import sleep
import requests


class BaseCrawler():

    def post_to_jobdata(self, title, page_new, html_text, crawler_id, tld):
        job_html_b64 = base64.b64encode(html_text)
        r = requests.post("http://localhost:8001/crawler_agent_post/",
                data={'crawler_id': crawler_id,
                    'tld': tld,
                    'job_page_url': page_new,
                    'job_title': title,
                    'job_html_b64': job_html_b64})
        return r.status_code, r.reason, str(r.text.encode('utf-8'))

    def page_get_html(self, title, page_new, crawler_id, tld):
        try:
            r = requests.get(page_new)
            if r.status_code == 200:
                html_text = str(r.text.encode('utf-8'))
                sleep(10)
                return html_text
        except Exception as e:
            print 'error', e
            pass
        else:
            pass
