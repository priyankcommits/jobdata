import argparse
import requests
import json
from BeautifulSoup import BeautifulSoup
from base_crawler import BaseCrawler

parser = argparse.ArgumentParser(description='Arguments for indeed.py')
parser.add_argument('-i', '--id', help='Input crawler agent id', required=True)
args = parser.parse_args()
crawler_id = args.id
keys = ['django', 'rails', 'angular', 'php', 'mysql']
locations = ['San_Diego%2C+CA', 'San+Francisco%2C+CA', 'New+York%2C+NY', 'Austin%2C+TX', 'Chicago%2C+IL', 'Philadelphia%2C+PA', 'Boston%2C+MA', 'Seattle%2C+WA', 'Dallas%2C+TX', 'Portland%2C+OR']
tld = 'indeed.com'


class IndeedScript(BaseCrawler):

    def main(self):
        for key in keys:
            for location in locations:
                for i in range(1, 5):
                    url = 'http://www.indeed.com/jobs?q=' + key + '&l=' + location + '&start=' + str((i-1)*10)
                    r = requests.get(url)
                    if r.status_code == 200:
                        soup = BeautifulSoup(r.text)
                        data = soup.findAll('h2', attrs={'class': 'jobtitle'})
                        for i in data:
                            page = str(i.a.get('href'))
                            page_new = 'https://www.indeed.com{0}'.format(page)
                            if page_new and page_new != 'None':
                                try:
                                    r = requests.post("http://localhost:8001/crawler_agent_check/",
                                        data={'crawler_id': crawler_id, 'job_page_url': page_new})
                                    if str(r.text.encode('utf-8')) == "True":
                                        page_new_r = requests.get(page_new)
                                        if self.tld_check(str(page_new_r.url), tld) == "True":
                                            print str(page_new_r.url)
                                            #html = self.page_get_html(page_new)
                                            html = str(page_new_r.text.encode('utf-8'))
                                            title = self.get_title(html)['title']
                                            html_text = html
                                            result = self.post_to_jobdata(title, page_new, html_text, crawler_id, tld)
                                            result_json = json.loads(result[2])
                                            job = int(result_json['job'])
                                            title_xpath = '//*[@id="job_header"]/b/font'
                                            location_xpath = '//*[@id="job_summary"]/p[1]/b[2]'
                                            nature_xpath = '//*[@id="job_summary"]/p[1]/b[3]'
                                            desc_xpath = '//*[@id="job-content"]'
                                            extracted = self.post_to_data_extract(title_xpath, location_xpath, nature_xpath, desc_xpath, html_text, job)
                                            print "Page Crawled " + page_new_r.url.encode('utf-8')
                                            print "Page First Hit: " + page_new
                                            print result
                                            print "Data Status: " + extracted
                                        else:
                                            print "Page First hit: " + page_new
                                            print "Page Hit: " + page_new_r.url
                                            print "TLD not in Domain"

                                    else:
                                        print page_new_r.url
                                        print "Page previously crawled"
                                except Exception as e:
                                    print page_new
                                    print e


if __name__ == "__main__":
    script = IndeedScript()
    script.main()
