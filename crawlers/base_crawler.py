import requests
import os
api_host = os.getenv('API_HOST', 'http://127.0.0.1:8001')


class BaseCrawler(object):

    def post_page(self, page_trimmed, page, crawler_id, tld, title_xpath, location_xpath, nature_xpath, desc_xpath):
        endpoint = "{0}/api_crawler_agent_post/".format(api_host)
        response = requests.post(
                endpoint,
                data={
                    'page_trimmed': page_trimmed,
                    'page': page,
                    'crawler_id': crawler_id,
                    'tld': tld,
                    'title_xpath': title_xpath,
                    'location_xpath': location_xpath,
                    'nature_xpath': nature_xpath,
                    'desc_xpath': desc_xpath,
                    }
                )

        return response.text
