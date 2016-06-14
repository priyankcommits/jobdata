import urllib2
import argparse

from BeautifulSoup import BeautifulSoup
from base_crawler import links_html

parser = argparse.ArgumentParser(description='Arguments for dicescript.py')
parser.add_argument('-i', '--id', help='Input crawler agent id', required=True)
args = parser.parse_args()
crawler_id = args.id
key = 'django'
locations = ['San+Francisco%2C+CA', 'New+York%2C+NY']
tld = 'dice.com'


class DiceScript():

    def main(self):
        for location in locations:
            url = 'https://www.dice.com/jobs?q=' + key + '&l=' + location + '&searchid=7665648499969'
            text = urllib2.urlopen(url).read()
            soup = BeautifulSoup(text)
            data = soup.findAll('div', attrs={'class': 'serp-result-content'})
            for i in data:
                page = str(i.h3.a.get('href'))
                page_new = page.replace('https:', 'http:')
                if page_new and page_new != 'None':
                    links_html(page_new, crawler_id, url, tld)

if __name__ == "__main__":
    script = DiceScript()
    script.main()
