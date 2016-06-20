import argparse
import requests
from BeautifulSoup import BeautifulSoup
from base_crawler import BaseCrawler

parser = argparse.ArgumentParser(description='Arguments for dicescript.py')
parser.add_argument('-i', '--id', help='Input crawler agent id', required=True)
args = parser.parse_args()
crawler_id = args.id
key = 'django'
locations = ['San_Francisco%2C_CA', 'New_York%2C_NY', 'San_Diego%2C_CA', 'Austin%2C_TX', 'Chicago%2C_IL']
tld = 'dice.com'


class DiceScript():

    def main(self):
        for location in locations:
            for i in range(1, 5):
                url = 'https://www.dice.com/jobs/q-' + key + '-limit-30-l-' + location + '-radius-30-startPage-' + str(i) + '-limit-30-jobs?searchid=8645363592122'
                r = requests.get(url)
                if r.status_code == 200:
                    soup = BeautifulSoup(r.text)
                    data = soup.findAll('div', attrs={'class': 'serp-result-content'})
                    for i in data:
                        page = str(i.h3.a.get('href'))
                        page_new = page.replace('https:', 'http:')
                        if page_new and page_new != 'None':
                            r = requests.post("http://localhost:8001/crawler_agent_check/",
                                    data={'crawler_id': crawler_id, 'job_page_url': page_new})
                            if str(r.text.encode('utf-8')) == "True":
                                page_new_request = requests.get(page_new)
                                soup_page_new = BeautifulSoup(page_new_request.text)
                                title = soup_page_new.findAll('title')
                                base_crawler = BaseCrawler()
                                html_text = base_crawler.page_get_html(title, page_new, crawler_id, tld)
                                result = base_crawler.post_to_jobdata(title, page_new, html_text, crawler_id, tld)
                                print page_new
                                print result
                            else:
                                print page_new
                                print "Page previously crawled"

if __name__ == "__main__":
    script = DiceScript()
    script.main()
