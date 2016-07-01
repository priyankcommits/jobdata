import argparse
import requests
from BeautifulSoup import BeautifulSoup
from base_crawler import BaseCrawler

parser = argparse.ArgumentParser(description='Arguments for indeed.py')
parser.add_argument('-i', '--id', help='Input crawler agent id', required=True)
args = parser.parse_args()
crawler_id = args.id
keys = ['django', 'rails', 'angular', 'php', 'mysql']
locations = ['San_Diego%2C+CA', 'San+Francisco%2C+CA', 'New+York%2C+NY', 'Austin%2C+TX', 'Chicago%2C+IL', 'Philadelphia%2C+PA', 'Boston%2C+MA', 'Seattle%2C+WA', 'Dallas%2C+TX', 'Portland%2C+OR']
tld = 'indeed.com'
keys_locations = [(k, l) for k in keys for l in locations]
url = 'http://www.indeed.com/jobs?q={0}&l={1}&start={2}'
title_xpath = '//*[@id="job_header"]/b/font//text()'
location_xpath = '//*[@id="job_header"]/span[2]//text()'
nature_xpath = '//*[@id="job_header"]//text()[2]'
desc_xpath = '//*[@id="job-content"]//text()'


class IndeedScript(BaseCrawler):

    def main(self):
        for key, location in keys_locations:
            for page_no in range(1, 5):
                page_url = url.format(key, location, str((page_no-1))*10)
                response = requests.get(page_url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text)
                    links = soup.findAll('h2', attrs={'class': 'jobtitle'})
                    for link in links:
                        page = str(link.a.get('href'))
                        page_new = 'https://www.indeed.com{0}'.format(page)
                        print page_new
                        if page_new and page_new is not 'None':
                            page_trimmed = page_new
                            print page_trimmed
                            status = self.post_page(
                                    page_trimmed, page_new, crawler_id,
                                    tld, title_xpath, location_xpath,
                                    nature_xpath, desc_xpath,
                                    )
                            print status

if __name__ == "__main__":
    script = IndeedScript()
    script.main()
