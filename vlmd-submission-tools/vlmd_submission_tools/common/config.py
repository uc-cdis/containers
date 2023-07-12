import os

HOST_NAME = os.environ.get('GEN3_HOSTNAME')
NAMESPACE="argo"
BASE_IMAGE = "quay.io/cdis/python:python3.9-data-science-master"

# Client-credentials secrets names/keys should also be in the configmap
# These might be rotated by the cloud-auto cron job client-create-rotate.
CLIENT_SECRET_NAME="vlmd-client-secret"
CLIENT_ID_CONFIG="ClientIdKey"
CLIENT_KEY_CONFIG="ClientSecretKey"
