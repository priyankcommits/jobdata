import argparse
import requests
import json
from BeautifulSoup import BeautifulSoup
from base_crawler import BaseCrawler

parser = argparse.ArgumentParser(description='Arguments for dicescript.py')
parser.add_argument('-i', '--id', help='Input crawler agent id', required=True)
args = parser.parse_args()
crawler_id = args.id
keys = ['django', 'rails', 'angular', 'php', 'mysql']
locations = ['San_Francisco%2C_CA', 'New_York%2C_NY', 'San_Diego%2C_CA', 'Austin%2C_TX', 'Chicago%2C_IL', 'Philadelphia%2C_PA', 'Boston%2C_MA', 'Seattle%2C_WA', 'Dallas%2C_TX', 'Portland%2C_OR']
tld = 'dice.com'

keys_locations = [(k,l) for k in keys for l in locations]
url = (
        'https://www.dice.com/jobs/q-{0}-limit-30-l-{1}-radius-30-startPage-'
        '{2}-limit-30-jobs?searchid=8645363592122'
       )

class DiceScript(BaseCrawler):

    def main(self):
        for key, location in keys_locations:
            for i in range(1, 5):
                url.format(key, location, i)
                response = requests.get(url)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.text)
                    links = soup.findAll('div', attrs={'class': 'serp-result-content'})
                    for link in links:
                        page = str(i.h3.a.get('href'))
                        page_new = page.replace('https:', 'http:')
                        if page_new and page_new != 'None':
                            if self.tld_check(page_new, tld) == "True":
                                r = requests.post("http://localhost:8001/crawler_agent_check/",
                                        data={'crawler_id': crawler_id, 'job_page_url': page_new})
                                if str(r.text.encode('utf-8')) == "True":
                                    html = self.page_get_html(page_new)
                                    title = html['title']
                                    html_text = html['r'].text.encode('utf-8')
                                    result = self.post_to_jobdata(title, page_new, html_text, crawler_id, tld)
                                    result_json = json.loads(result[2])
                                    job = int(result_json['job'])
                                    title_xpath = '//*[@id="jt"]'
                                    location_xpath = '//*[@id="header-wrap"]/div[2]/div/div[1]/ul/li[2]'
                                    nature_xpath = '//*[@id="bd"]/div[2]/div[1]/div[2]/div/div[2]/span'
                                    desc_xpath = '//*[@id="jobdescSec"]'
                                    extracted = self.post_to_data_extract(title_xpath, location_xpath, nature_xpath, desc_xpath, html_text, job)
                                    print "Page Crawled" + html['r'].url.encode('utf-8')
                                    print "Page First Hit:" + page_new
                                    print result
                                    print "Data Status:" + extracted
                                else:
                                    print page_new
                                    print "Page previously crawled"
                            else:
                                print "Page First Hit" + page_new
                                print "TLD not in Domain"

if __name__ == "__main__":
    script = DiceScript()
    script.main()
