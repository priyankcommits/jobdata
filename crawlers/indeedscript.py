import argparse
import requests
from BeautifulSoup import BeautifulSoup
from base_crawler import BaseCrawler

parser = argparse.ArgumentParser(description='Arguments for indeed.py')
parser.add_argument('-i', '--id', help='Input crawler agent id', required=True)
args = parser.parse_args()
crawler_id = args.id
keys = ['django','rails','angular','php','mysql']
locations = ['San+Francisco%2C+CA', 'New+York%2C+NY', 'San_Diego%2C+CA', 'Austin%2C+TX', 'Chicago%2C+IL','Philadelphia%2C+PA','Boston%2C+MA','Seattle%2C+WA','Dallas%2C+TX','Portland%2C+OR']
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
                            if page_new and page_new is not 'None':
                                if self.tld_check(page_new, tld) == "True":
                                    r = requests.post("http://localhost:8001/crawler_agent_check/",
                                            data={'crawler_id': crawler_id, 'job_page_url': page_new})
                                    if str(r.text.encode('utf-8')) == "True":
                                        page_new_request = requests.get(page_new)
                                        soup_page_new = BeautifulSoup(page_new_request.text)
                                        title = soup_page_new.findAll('title')
                                        html = self.page_get_html(title, page_new, crawler_id, tld)
                                        html_text = html.text.encode('utf-8')
                                        result = self.post_to_jobdata(title, page_new, html_text, crawler_id, tld)
                                        extracted = self.post_to_data_extract(title_xpath, location_xpath, nature_xpath_desc_xpath, job)
                                        print "Page Crawled" + html.url
                                        print "Page First Hit" + page_new
                                        print result
                                        print extracted
                                    else:
                                        print page_new
                                        print "Page previously crawled"
                                else:
                                    print "Page First Hit" + page_new
                                    print "TLD not in Domain"

if __name__ == "__main__":
    script = IndeedScript()
    script.main()
