from gcloud_storage import GcloudStorage

gcs = GcloudStorage()

gcs_obs = gcs.list_objects()

list_obs = list(gcs_obs)

print list_obs

print list_obs[1]

print gcs.generate_signed_url(list_obs[1])
