import base64
from unittest.mock import MagicMock, patch

import json
import pytest
import requests

from vlmd_submission_tools.common import utils

class TestCommonsUtils():

    @patch('kubernetes.config.load_kube_config')
    @patch('kubernetes.client.CoreV1Api.read_namespaced_secret')
    def test_get_client_secret(self, mocked_kube_client, mocked_kube_config):
        # method should parse out the client_id and client_secret from the kubernetes secret
        client_secret_name="my_g3auto_secret"
        client_secret_key="fence_client_credentials.json"
        client_id_config="my_client_id"
        client_secret_config="my_client_secret"
        namespace = "default"

        expected_client_id = "test_client_id"
        expected_client_key = "test_client_key"

        expected_secret_json = {
            client_id_config: expected_client_id,
            client_secret_config: expected_client_key
        }
        mocked_kube_secret = json.dumps(expected_secret_json).encode('utf-8')
        mocked_kube_secret = base64.b64encode(mocked_kube_secret)
        mocked_kube_client.return_value = MagicMock(data={client_secret_key: mocked_kube_secret})
        mocked_kube_config.return_value = MagicMock()

        response = utils.get_client_secret(
            client_secret_name, client_secret_key, client_id_config, client_secret_config, namespace
        )
        assert response == (expected_client_id, expected_client_key)


    @patch('requests.get')
    def test_check_mds_study_id(self, mocked_post):
        # method should parse the existing data dictionaries out of a mds request
        hostname = "mycommons.planx-pla.net"
        study_id = "my_study_id"
        expected_data_dictionaries = {
            "data_dictionaries" : {
                "my first dictionary": "guid1",
                "my second dictionary": "guid2"
            }
        }
        mock_mds_response = MagicMock(requests.Response)
        mock_mds_response.status_code = 200
        mock_mds_response.json.return_value = {
            "_guid_type": "discovery_metadata",
            "variable_level_metadata": expected_data_dictionaries
        }
        mocked_post.return_value = mock_mds_response

        result = utils.check_mds_study_id(study_id, hostname)
        assert result == expected_data_dictionaries


    @patch('requests.get')
    def test_check_mds_study_id_exception(self, mocked_post):
        # test study_id is missing or _guid_type is not 'discovery_metadata'

        hostname = "mycommons.planx-pla.net"
        study_id = "my_study_id"
        expected_data_dictionaries = {
            "my first dictionary": "guid1",
            "my second dictionary": "guid2"
        }
        # mds returns 404
        mock_mds_response = MagicMock(requests.Response)
        mock_mds_response.status_code = 404
        mock_mds_response.json.return_value = {
            "_guid_type": "discovery_metadata",
            "data_dictionaries": expected_data_dictionaries
        }
        mocked_post.return_value = mock_mds_response
        expected_error = f"Study ID {study_id} not found in MDS"
        with pytest.raises(ValueError, match=expected_error):
            utils.check_mds_study_id(study_id, hostname)

        # _guid_type is not discovery_metadata
        mock_mds_response.status_code = 200
        mock_mds_response.json.return_value = {
            "_guid_type": "some_other_guid_type",
            "data_dictionaries": expected_data_dictionaries
        }
        mocked_post.return_value = mock_mds_response
        expected_error = "Study ID is not dicovery metadata"
        with pytest.raises(ValueError, match=expected_error):
            utils.check_mds_study_id(study_id, hostname)


    @patch('requests.post')
    def test_get_client_token(self, mocked_post):
        # method should parse out the token from the fence response
        hostname = "mycommons.planx-pla.net"
        client_id = "client_id"
        client_secret = "client_secret"
        expected_token = "my_token"
        # mock the fence response for requesting token
        mock_fence_response = MagicMock(requests.Response)
        mock_fence_response.status_code = 200
        mock_fence_response.json.return_value = {"access_token": expected_token}
        mocked_post.return_value = mock_fence_response

        result = utils.get_client_token(hostname, client_id, client_secret)
        assert result == expected_token
