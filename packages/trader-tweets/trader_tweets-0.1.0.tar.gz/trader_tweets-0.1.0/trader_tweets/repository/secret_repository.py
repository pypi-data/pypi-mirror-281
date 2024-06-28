import os

from google.cloud import secretmanager


def fetch_secret(secret_name, secret_version):
    # connect to gcp secret manager
    client = secretmanager.SecretManagerServiceClient()
    project_id = os.environ['GCP_PROJECT_ID']
    name = client.secret_version_path(project=project_id, secret=secret_name, secret_version=secret_version)
    response = client.access_secret_version(name=name)
    return response.payload.data.decode('UTF-8')


class SecretRepository:
    pass
