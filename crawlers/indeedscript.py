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
locations = ['San+Francisco%2C+CA', 'New+York%2C+NY', 'San_Diego%2C+CA', 'Austin%2C+TX', 'Chicago%2C+IL', 'Philadelphia%2C+PA', 'Boston%2C+MA', 'Seattle%2C+WA', 'Dallas%2C+TX', 'Portland%2C+OR']
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
                                import ipdb;ipdb.set_trace();
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
    script = IndeedScript()
    script.main()
