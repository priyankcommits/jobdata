import os
import uuid
import json
import time
import HTMLParser
import urllib2
from lxml import etree
from datetime import datetime

from django.utils.html import strip_tags

from gcloud_storage import GcloudStorage
from io import StringIO

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
    import ipdb;ipdb.set_trace();
    data_list = []
    file = open("something.html", "w+")
    file.write(str(html.encode('utf-8')))
    file.close()
    try:
        for xpath in xpath_list:
            xpath = xpath.encode('utf-8')
            tree = etree.HTML(html)
            result = tree.xpath(xpath + '//text()')
            if result:
                stripped_text = strip_tags(str(result[0]))
                stripped_text = stripped_text.replace('\n', '')
                stripped_text = stripped_text.replace('\t', '')
            else:
                stripped_text = ''
            data_list.append(stripped_text)

        return data_list
    except Exception as e:
        print e
        return 0

def strip_data_old(xpath_list, html):
    import ipdb;ipdb.set_trace();
    data_list = []
    file = open("something.html", "w+")
    file.write(str(html.encode('utf-8')))
    file.close()
    xpath_temp = [xpath_list[0], xpath_list[3]]
    try:
        for xpath in xpath_temp:
            xpath = xpath.encode('utf-8')
            htmlparser = etree.HTMLParser()
            tree = etree.parse(StringIO(html), htmlparser)
            result = tree.xpath(xpath)
            stripped_text = strip_tags(etree.tostring(result[0]))
            stripped_text = stripped_text.replace('\n', '')
            stripped_text = stripped_text.replace('\t', '')
            data_list.append(stripped_text)

        return data_list
    except Exception as e:
        print e
        return 0
