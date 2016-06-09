import urllib2
import base64
import sys
from time import sleep

import requests
from BeautifulSoup import BeautifulSoup

id = sys.argv[1]
key = 'django'
locations = ['San+Francisco%2C+CA', 'New+York%2C+NY']
tld = 'dice.com'


def post_to_jobdata(html_text):
    job_html_b64 = base64.b64encode(html_text)
    r = requests.post("http://localhost:8000/crawler_agent_post/",data={'id': id,'tld': tld,'job_url': url,'job_html_b64': job_html_b64})
    print(r.status_code, r.reason, str(r.text))
for location in locations:
    locale = location
    url = 'https://www.dice.com/jobs?q=' + key + '&l=' + locale + '&searchid=7665648499969'
    text = urllib2.urlopen(url).read()
    soup = BeautifulSoup(text)
    data = soup.findAll('div', attrs={'class': 'serp-result-content'})
    for i in data:
        page = str(i.h3.a.get('href'))
        page_new = page.replace('https:', 'http:')
        if page_new and page_new != 'None':
            r = requests.get(page_new)
            if r.status_code == 200:
                html = urllib2.urlopen(page_new)
                html_text = str(html.read())
                post_to_jobdata(html_text)
                html.close()
                sleep(10)
                print locale
