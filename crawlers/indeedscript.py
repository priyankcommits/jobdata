import argparse
import requests
from BeautifulSoup import BeautifulSoup
from base_crawler import BaseCrawler

parser = argparse.ArgumentParser(description='Arguments for indeed.py')
parser.add_argument('-i', '--id', help='Input crawler agent id', required=True)
args = parser.parse_args()
crawler_id = args.id
key = 'django'
locations = ['San+Francisco%2C+CA', 'New+York%2C+NY','San+Diego%2C+CA', 'Austin%2C+TX', 'Chicago%2C+IL']
tld = 'indeed.com'


class IndeedScript(BaseCrawler):

    def main(self):
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
                            r = requests.post("http://localhost:8001/crawler_agent_check/",
                                    data={'crawler_id': crawler_id, 'job_page_url': page_new})
                            if str(r.text.encode('utf-8')) == "True":
                                try:
                                    page_new_request = requests.get(page_new)
                                    soup_page_new = BeautifulSoup(page_new_request.text)
                                    title = soup_page_new.findAll('title')
                                    html_text = self.page_get_html(title, page_new, crawler_id, tld)
                                    result = self.post_to_jobdata(title, page_new, html_text, crawler_id, tld)
                                    print page_new
                                    print result
                                except Exception as e:
                                    print "Error", e
                                    pass
                            else:
                                print page_new
                                print "Page previously crawled"

if __name__ == "__main__":
    script = IndeedScript()
    script.main()
