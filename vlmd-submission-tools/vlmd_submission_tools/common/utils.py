import base64
import json
import os
import requests

import kubernetes

from vlmd_submission_tools.common import config


def get_client_secret(
    client_secret_name=config.CLIENT_SECRET_NAME,
    client_secret_key=config.CLIENT_SECRET_KEY_CONFIG,
    client_id_config=config.CLIENT_ID_CONFIG,
    client_secret_config=config.CLIENT_KEY_CONFIG,
    namespace=config.NAMESPACE
):
    """
    Read fence client_id and client_secret from kubernetes secret with the following format
    {
        client_secret_key:
        {
          client_id_config: <client_id>,
          client_secret_config: <client_secret>
        }
    }
    """
    kube_client = get_kube_client()
    secret = kube_client.read_namespaced_secret(client_secret_name, namespace)
    secret = secret.data[client_secret_key]
    secret_json = json.loads(base64.b64decode(secret).decode('ascii'))
    client_id = secret_json[client_id_config]
    client_secret = secret_json[client_secret_config]
    return client_id, client_secret


def get_kube_client():
    if os.environ.get('KUBERNETES_SERVICE_HOST'):
        # Use this for running in cluster
        kubernetes.config.load_incluster_config()
    else:
        # Use this for running locally
        kubernetes.config.load_kube_config()

    kube_client = kubernetes.client.CoreV1Api()

    return kube_client


def check_mds_study_id(study_id, hostname=config.HOST_NAME):
    try:
        url = f"https://{hostname}/mds/metadata/{study_id}"
        response = requests.get(url)
    except:
        raise Exception("Could not get study ID metadata")

    if response.status_code != 200:
        raise ValueError(f"Study ID {study_id} not found in MDS")
    if response.json().get("_guid_type") != "discovery_metadata":
        raise ValueError("Study ID is not dicovery metadata")

    existing_data_dictionaries = response.json().get("data_dictionaries", {})

    return existing_data_dictionaries


def get_client_token(hostname: str, client_id: str, client_secret: str):
    try:
        token_url = f"https://{hostname}/user/oauth2/token"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = {'grant_type': 'client_credentials'}
        data = 'scope=openid user data'

        token_result = requests.post(
            token_url, params=params, headers=headers, data=data,
            auth=(client_id, client_secret),
        )
        token =  token_result.json()["access_token"]

    except:
        raise Exception("Could not get token")

    return token
