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
