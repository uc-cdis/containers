import os

HOST_NAME = os.environ.get('GEN3_HOSTNAME')
NAMESPACE="default"
BASE_IMAGE = "quay.io/cdis/python:python3.9-data-science-master"

# Client-credentials secrets names/keys could also be stored in the configmap.
# These might be rotated by the cloud-auto cron job client-create-rotate.
CLIENT_SECRET_NAME="VLMD_CLIENT_SECRET"
CLIENT_ID_CONFIG="client_id"
CLIENT_KEY_CONFIG="client_secret"
