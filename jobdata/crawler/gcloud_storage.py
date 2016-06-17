# Wrapper aroung gcloud library

import time
import os
from gcloud import storage

keyfile_path = os.getenv('GCLOUD_KEY_PATH')
project = 'bcode-job-data-dev'
bucket_name = 'job-data-development'

# client = storage.Client.from_service_account_json(keyfile_path,
        # project=project)
# bucket = client.get_bucket(bucket_name)
# blob = bucket.blob('content.json')
# content = {}
# blob.upload_from_string(content)

class GcloudStorage(object):

    def __init__(self):
        try:
            self.client = storage.Client.from_service_account_json(keyfile_path,
                    project=project)
        except Exception as e:
            # log error
            # type of exception
            print type(e)
            # error message
            print e.message

    def get_bucket(self, bucket_name):
        bucket = self.client.get_bucket(bucket_name)

        return bucket

    def list_objects(self, bucket_name=bucket_name):
        # returns an iterator
        try:
            bucket = self.get_bucket(bucket_name)

            return bucket.list_blobs()
        except Exception as e:
            # log error
            # type of exception
            print type(e)
            # error message
            print e.message

    def create_object_from_string(self, path, content_string):
        # what should it return?
        bucket = self.get_bucket(bucket_name)
        blob = bucket.blob(path)
        blob.upload_from_string(content_string)

    def generate_signed_url(self, blob, expiration_time=100):
        expiry_time = int(time.time())
        return blob.generate_signed_url(expiry_time + expiration_time)
