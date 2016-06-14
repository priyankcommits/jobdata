import urllib2
import argparse

from BeautifulSoup import BeautifulSoup
from base_crawler import links_html

parser = argparse.ArgumentParser(description='Arguments for dicescript.py')
parser.add_argument('-i', '--id', help='Input crawler agent id', required=True)
args = parser.parse_args()
crawler_id = args.id
key = 'software'
tld = 'gladwinanalytics.com'


class GladWinScript():

    def main(self):
        url = 'http://www.gladwinanalytics.com/jobs?q=' + key
        text = urllib2.urlopen(url).read()
        soup = BeautifulSoup(text)
        data = soup.findAll('div', attrs={'class': 'job_tlt_left'})
        for i in data:
            page = str(i.a.get('href'))
            page_new = page
            if page_new and page_new != 'None':
                links_html(page_new, crawler_id, url, tld)

if __name__ == "__main__":
    script = GladWinScript()
    script.main()
