import argparse
import requests
from BeautifulSoup import BeautifulSoup
from base_crawler import BaseCrawler

parser = argparse.ArgumentParser(description='Arguments for dicescript.py')
parser.add_argument('-i', '--id', help='Input crawler agent id', required=True)
args = parser.parse_args()
crawler_id = args.id
keys = ['software', 'php', 'mysql', 'java', 'bigdata']
tld = 'gladwinanalytics.com'
url = 'http://www.gladwinanalytics.com/jobs?q={0}&p={1}'
title_xpath = '/html/body/div[5]/div[1]/div/div/div[1]/div[2]/div/div[2]/h1'
location_xpath = '/html/body/div[5]/div[1]/div/div/div[1]/div[2]/div/div[2]/h4/span'
nature_xpath = '/html/body/div[5]/div[1]/div/div/div[1]/div[2]/div/div[2]/p[3]/span'
desc_xpath = '/html/body/div[5]/div[1]/div/div/div[1]/div[3]/div/div[1]'


class GladWinScript(BaseCrawler):


   def main(self):
        for key in keys:
            for page_no in range(1, 25):
                page_url = url.format(key, str(page_no))
                response = requests.get(page_url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text)
                    links = soup.findAll('div', attrs={'class': 'job_tlt_left'})
                    for link in links:
                        page = str(link.a.get('href'))
                        page_new = page
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
    script = GladWinScript()
    script.main()
