import urllib2
import argparse

from BeautifulSoup import BeautifulSoup
from base_crawler import BaseCrawler

parser = argparse.ArgumentParser(description='Arguments for agenlistscript.py')
parser.add_argument('-i', '--id', help='Input crawler agent id', required=True)
args = parser.parse_args()
crawler_id = args.id
key = 'django'
locations = ['Hyderabad', 'Bangalore']
tld = 'angellist.co'


class AngelListScript():

    def main(self):
        for location in locations:
            url = 'https://angel.co/jobs#find/f!%7B%22roles%22%3A%5B%22' + key + '%22%5D%2C%22types%22%3A%5B%22full-time%22%5D%2C%22locations%22%3A%5B%22' + location + '%22%5D%7D'
            opener = urllib2.build_opener()
            opener.addheaders = [('User-agent', 'Mozilla/5.0')]
            response = opener.open(url)
            text = response.read()
            soup = BeautifulSoup(text)
            data = soup.findAll('div', attrs={'class': 'listing-row'})
            for i in data:
                page = str(i.div.div.a.get('href'))
                page_new = page
                if page_new and page_new != 'None':
                    base_crawler = BaseCrawler()
                    base_crawler.links_html(page_new, crawler_id, url, tld)

if __name__ == "__main__":
    script = AngelListScript()
    script.main()
