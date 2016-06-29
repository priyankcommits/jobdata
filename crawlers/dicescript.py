import argparse
import requests
from BeautifulSoup import BeautifulSoup
from base_crawler import BaseCrawler

parser = argparse.ArgumentParser(description='Arguments for dicescript.py')
parser.add_argument('-i', '--id', help='Input crawler agent id', required=True)
args = parser.parse_args()
crawler_id = args.id
keys = ['django', 'rails', 'angular', 'php', 'mysql']
locations = ['San_Francisco%2C_CA', 'New_York%2C_NY', 'San_Diego%2C_CA', 'Austin%2C_TX', 'Chicago%2C_IL', 'Philadelphia%2C_PA', 'Boston%2C_MA', 'Seattle%2C_WA', 'Dallas%2C_TX', 'Portland%2C_OR']
tld = 'dice.com'
keys_locations = [(k, l) for k in keys for l in locations]
url = (
        'https://www.dice.com/jobs/q-{0}-limit-30-l-{1}-radius-30-startPage-'
        '{2}-limit-30-jobs?searchid=8645363592122'
       )
title_xpath = '//*[@id="jt"]'
location_xpath = '//*[@id="header-wrap"]/div[2]/div/div[1]/ul/li[2]'
nature_xpath = '//*[@id="bd"]/div[2]/div[1]/div[2]/div/div[2]/span'
desc_xpath = '//*[@id="jobdescSec"]'


class DiceScript(BaseCrawler):

    def main(self):
        for key, location in keys_locations:
            for page_no in range(1, 5):
                page_url = url.format(key, location, page_no)
                response = requests.get(page_url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text)
                    links = soup.findAll('div', attrs={'class': 'serp-result-content'})
                    for link in links:
                        page = str(link.h3.a.get('href'))
                        page_new = page.replace('https:', 'http:')
                        print page_new
                        if page_new and page_new is not 'None':
                            page_trimmed = page_new[:page_new.rfind("?"):]
                            print page_trimmed
                            status = self.post_page(
                                    page_trimmed, page_new, crawler_id,
                                    tld, title_xpath, location_xpath,
                                    nature_xpath, desc_xpath,
                                    )
                            print status
if __name__ == "__main__":
    script = DiceScript()
    script.main()
