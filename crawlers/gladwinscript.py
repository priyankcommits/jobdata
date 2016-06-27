import argparse
import requests
from BeautifulSoup import BeautifulSoup
from base_crawler import BaseCrawler

parser = argparse.ArgumentParser(description='Arguments for dicescript.py')
parser.add_argument('-i', '--id', help='Input crawler agent id', required=True)
args = parser.parse_args()
crawler_id = args.id
key = 'software'
tld = 'gladwinanalytics.com'


class GladWinScript(BaseCrawler):

    def main(self):
        for i in range(1, 25):
            url = 'http://www.gladwinanalytics.com/jobs?q=' + key + '&p=' + str(i)
            r = requests.get(url)
            if r.status_code == 200:
                soup = BeautifulSoup(r.text)
                data = soup.findAll('div', attrs={'class': 'job_tlt_left'})
                for i in data:
                    page = str(i.a.get('href'))
                    page_new = page
                    if page_new and page_new is not 'None':
                        r = requests.post("http://localhost:8001/crawler_agent_check/",
                                data={'crawler_id': crawler_id, 'job_page_url': page_new})
                        if str(r.text.encode('utf-8')) == "True":
                            page_new_request = requests.get(page_new)
                            soup_page_new = BeautifulSoup(page_new_request.text)
                            title = soup_page_new.findAll('title')
                            html_text = self.page_get_html(title, page_new, crawler_id, tld)
                            result = self.post_to_jobdata(title, page_new, html_text, crawler_id, tld)
                            print page_new
                            print result
                        else:
                            print page_new
                            print "Page previously crawled"

if __name__ == "__main__":
    script = GladWinScript()
    script.main()

import argparse
import requests
import json
from BeautifulSoup import BeautifulSoup
from base_crawler import BaseCrawler

parser = argparse.ArgumentParser(description='Arguments for gladwinscript.py')
parser.add_argument('-i', '--id', help='Input crawler agent id', required=True)
args = parser.parse_args()
crawler_id = args.id
keys = ['django', 'rails', 'angular', 'php', 'mysql']
tld = 'gladwinanalytics.com'


class GladWinScript(BaseCrawler):

    def main(self):
        for key in keys:
            for i in range(1, 25):
                url = 'http://www.gladwinanalytics.com/jobs?q=' + key + '&p=' + str(i)
                r = requests.get(url)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text)
                    data = soup.findAll('div', attrs={'class': 'job_tlt_left'})
                    for i in data:
                        page = str(i.a.get('href'))
                        page_new = page
                        if page_new and page_new != 'None':
                            if self.tld_check(page_new, tld) == "True":
                                r = requests.post("http://localhost:8001/crawler_agent_check/",
                                        data={'crawler_id': crawler_id, 'job_page_url': page_new})
                                if str(r.text.encode('utf-8')) == "True":
                                    html = self.page_get_html(page_new)
                                    title = html['title']
                                    html_text = html['r'].text.encode('utf-8')
                                    result = self.post_to_jobdata(title, page_new, html_text, crawler_id, tld)
                                    result_json = json.loads(result[2])
                                    job = int(result_json['job'])
                                    title_xpath = '//*[@id="job_header"]/b/font'
                                    location_xpath = '//*[@id="job_summary"]/p[1]/b[2]'
                                    nature_xpath = '//*[@id="job_summary"]/p[1]/b[3]'
                                    desc_xpath = '//*[@id="job-content"]/tbody/tr/td[1]/table/tbody/tr/td'
                                    extracted = self.post_to_data_extract(title_xpath, location_xpath, nature_xpath, desc_xpath, html_text, job)
                                    print "Page Crawled" + html['r'].url.encode('utf-8')
                                    print "Page First Hit:" + page_new
                                    print result
                                    print "Data Status:" + extracted
                                else:
                                    print page_new
                                    print "Page previously crawled"
                            else:
                                print "Page First Hit" + page_new
                                print "TLD not in Domain"

if __name__ == "__main__":
    script = GladWinScript()
    script.main()
