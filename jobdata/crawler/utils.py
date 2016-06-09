import os
import uuid
import json
import time
from datetime import datetime

from gcloud_storage import GcloudStorage


def write_to_gcloud_storage(id, tld, job_url, job_html_b64):
    agent_dir = 'agent_id_' + str(id)
    date_dir = datetime.utcnow().strftime("%Y%m%d")
    path = agent_dir + '/' + date_dir
    data = {}
    data['crawler_agent_id'] = id
    data['tld'] = tld
    data['guid'] = str(uuid.uuid4())
    data['job_url'] = job_url
    data['job_html_b64'] = job_html_b64
    data['created_at'] = time.time()
    filepath = path + '/' + 'ts_' + str(data['guid']) + '.json'
    json_data = json.dumps(data)
    try:
        gcs = GcloudStorage()
        gcs.create_object_from_string(filepath, json_data)
    except:
        return "Failed to write to GCS"
    else:
        return "Wrote to gcloud storage"


def write_to_local_storage(id, tld, job_url, job_html_b64):
    base_dir = 'jobdata-development'
    agent_dir = 'agent_id_' + str(id)
    date_dir = datetime.utcnow().strftime("%Y%m%d")
    path = base_dir + '/' + agent_dir + '/' + date_dir
    if not os.path.exists(path):
        os.makedirs(path)
    data = {}
    data['crawler_agent_id'] = id
    data['tld'] = tld
    data['guid'] = str(uuid.uuid4())
    data['job_url'] = job_url
    data['job_html_b64'] = job_html_b64
    data['created_at'] = time.time()
    filepath = path + '/' + 'ts_' + str(data['guid']) + '.json'
    json_data = json.dumps(data)
    try:
        output = open(filepath, "wb")
        output.write(json_data)
        output.close()
    except:
        return "Failed to write to local storage"
    else:
        return "Wrote to local storage"
