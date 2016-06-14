import urllib2
import argparse

from BeautifulSoup import BeautifulSoup
from base_crawler import links_html

parser = argparse.ArgumentParser(description='Arguments for indeed.py')
parser.add_argument('-i', '--id', help='Input crawler agent id', required=True)
args = parser.parse_args()
crawler_id = args.id
key = 'django'
locations = ['San+Diego%2C+CA', 'Austin%2C+TX']
tld = 'indeed.com'


class IndeedScript():

    def main(self):
        for location in locations:
            url = 'http://www.indeed.com/jobs?q=' + key + '&l=' + location
            text = urllib2.urlopen(url).read()
            soup = BeautifulSoup(text)
            data = soup.findAll('h2', attrs={'class': 'jobtitle'})
            for i in data:
                page = str(i.a.get('href'))
                page_new = 'https://www.indeed.com{0}'.format(page)
                if page_new and page_new != 'None':
                    links_html(page_new, crawler_id, url, tld)

if __name__ == "__main__":
    script = IndeedScript()
    script.main()
