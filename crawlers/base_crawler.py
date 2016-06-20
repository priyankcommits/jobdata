import urllib2
import base64
from time import sleep

import requests


class BaseCrawler():

    def post_to_jobdata(self, title, page_new, html_text, crawler_id, url, tld):
        job_html_b64 = base64.b64encode(html_text)
        r = requests.post("http://localhost:8001/crawler_agent_post/",
                data={'crawler_id': crawler_id,
                    'tld': tld,
                    'job_parent_url': url,
                    'job_page_url': page_new,
                    'job_title': title,
                    'job_html_b64': job_html_b64})
        print(r.status_code, r.reason, str(r.text))

    def links_html(self, title, page_new, crawler_id, url, tld):
        print page_new
        try:
            r = requests.get(page_new)
            if r.status_code == 200:
                html = urllib2.urlopen(page_new)
                html_text = str(html.read())
                self.post_to_jobdata(title, page_new, html_text, crawler_id, url, tld)
                html.close()
                sleep(10)
        except Exception as e:
            print 'error', e
            pass
        else:
            pass
