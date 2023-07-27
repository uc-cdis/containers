import os

HOST_NAME = os.environ.get('GEN3_HOSTNAME')
BASE_IMAGE = "quay.io/cdis/python:python3.9-data-science-master"

# Names and keys for client-credentials secrets stored in a kubernetes secret.
# Example values:
# CLIENT_SECRET_NAME="vlmd-fence-client-g3auto"
# CLIENT_SECRET_KEY_CONFIG="fence_client_credentials.json"
# NAMESPACE="default"
CLIENT_SECRET_NAME=os.environ.get('CLIENT_SECRET_NAME')
CLIENT_SECRET_KEY_CONFIG=os.environ.get('CLIENT_SECRET_KEY_CONFIG')
NAMESPACE=os.environ.get('CLIENT_SECRET_NAMESPACE')
CLIENT_ID_CONFIG="client_id"
CLIENT_KEY_CONFIG="client_secret"
