import requests
import argparse
from BeautifulSoup import BeautifulSoup
from base_crawler import BaseCrawler

parser = argparse.ArgumentParser(description='Arguments for agenlistscript.py')
parser.add_argument('-i', '--id', help='Input crawler agent id', required=True)
args = parser.parse_args()
crawler_id = args.id

title_xpath = "/html/body/div[1]/div[2]/div/div[1]/h1"
location_xpath = "/html/body/div[1]/div[2]/div/div[1]/div[1]"
nature_xpath = "/html/body/div[1]/div[2]/div/div[1]/div[1]"
desc_xpath = "/html/body/div[1]/div[3]/div/div[2]/div"


class AngelListScript(BaseCrawler):

    def main(self):
        slugs = [
            'stripe', 'tinder', 'vsco', 'hinge' 'gustohq' 'brit-co-2', 'medium', 'uber',
            'ciphergraph-networks'
        ]
        for slug in slugs:
            url = "https://angel.co/{0}/jobs".format(slug)
            response = requests.get(url)
            if response.status_code is 200:
                soup = BeautifulSoup(response.text)
                links = soup.findAll(
                    'div', attrs={'class': 'listing-title s-grid-colSm18'}
                )
                for link in links:
                    href = link.findAll('a')[0].get('href')
                    print href
                    status = self.post_page(
                        href, href, crawler_id, tld,
                        title_xpath, location_xpath, nature_xpath, desc_xpath
                    )
                    print status


if __name__ == "__main__":
    script = AngelListScript()
    script.main()
