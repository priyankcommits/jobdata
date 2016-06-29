import os
import uuid
import json
import time
import requests
import base64
from lxml import etree
from io import StringIO
from datetime import datetime

from django.utils.html import strip_tags

from BeautifulSoup import BeautifulSoup
from gcloud_storage import GcloudStorage


def write_to_storage(crawler_id, tld, job_page_url, job_title, job_html_b64):
    base_dir = 'job-data-development'
    agent_dir = 'agent_id_' + str(crawler_id)
    date_dir = datetime.utcnow().strftime("%Y%m%d")
    data = {
            'crawler_agent_id': crawler_id,
            'tld': tld,
            'guid': str(uuid.uuid4()),
            'job_page_url': job_page_url,
            'job_title': job_title,
            'job_html_b64': job_html_b64,
            'created_at': time.time(),
            }
    json_data = json.dumps(data)
    if os.getenv('STORAGE_DATA') == 'development':
        path = "{0}/{1}".format(agent_dir, date_dir)
        filepath = path + '/' + str(data['created_at']) + '_' + str(data['guid']) + '.json'
        try:
            gcs = GcloudStorage()
            gcs.create_object_from_string(filepath, json_data)
        except Exception as e:
            return {'status': str(e)}
        else:
            return {'status': 'Wrote to gcloud storage', 'path': filepath}
    elif os.getenv('STORAGE_DATA') == 'local':
        path = "{0}/{1}/{2}".format(base_dir, agent_dir, date_dir)
        if not os.path.exists(path):
            os.makedirs(path)
        filepath = path + '/' + str(data['created_at']) + '_' + str(data['guid']) + '.json'
        output = open(filepath, "wb")
        try:
            output.write(json_data)
            output.close()
        except Exception as e:
            return {'status': str(e)}
        else:
            return {'status': 'Wrote to local storage'}
    else:
        return {'status': 'Could not find environment'}


def strip_data(xpath_list, html):
    data_list = []
    try:
        for xpath in xpath_list:
            xpath = xpath.encode('utf-8')
            tree = etree.HTML(html)
            result = tree.xpath(xpath)
            if result:
                stripped_text = strip_tags(etree.tostring(result[0]))
                stripped_text = stripped_text.replace('\n', '')
                stripped_text = stripped_text.replace('\t', '')
            else:
                if xpath_list[0] or xpath[3]:
                    return 0
                else:
                    stripped_text = ''
            data_list.append(stripped_text)

        return data_list
    except:
        return 0


def page_get_html(page):
    try:
        response = requests.get(page)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text)
            title = soup.find('title').getText()

            return {'text': response.text, 'title': title}
    except Exception as e:
        print 'error', e
        return 0


def tld_check(tld, page):
    if tld in page[:30]:
        return "True"
    else:
        return "False"


def convert_to_b64(html):
    html_text = html.encode('utf-8')

    return base64.b64encode(str(html_text))
