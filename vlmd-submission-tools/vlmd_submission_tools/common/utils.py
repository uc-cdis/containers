import json
import os
import requests


from vlmd_submission_tools.common import config

def get_client_secret():
    """The fence client-credentials are read from JSON in an environment variable"""
    fence_client_secret = json.loads(os.environ.get(config.CLIENT_SECRET_NAME))
    client_id = fence_client_secret[config.CLIENT_ID_CONFIG]
    client_secret = fence_client_secret[config.CLIENT_KEY_CONFIG]

    return client_id, client_secret


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
