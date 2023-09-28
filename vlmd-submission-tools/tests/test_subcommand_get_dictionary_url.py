"""Tests for the ``vlmd_submission_tools.subcommands.HelloWorld`` subcommand"""
import os
from typing import NamedTuple
from unittest.mock import MagicMock, patch
from urllib.parse import quote

import json
import pytest
import requests
from utils import cleanup_files

from vlmd_submission_tools.subcommands import GetDictionaryUrl


class MockArgs(NamedTuple):
    data_dict_guid: str
    output: str


class TestGetDictionaryUrlSubcommand:

    def get_mock_args(self):
        return MockArgs(
            data_dict_guid="indexd_guid",
            output="url_output.json",
        )


    @patch('requests.get')
    @patch('vlmd_submission_tools.common.utils.get_client_secret')
    @patch('vlmd_submission_tools.common.utils.get_client_token')
    def test_get_dictionary_url(self, mocked_client_token, mocked_client_secret, mocked_request):

        args = self.get_mock_args()

        hostname = "mycommons.planx-pla.net"
        data_dict_guid = args.data_dict_guid
        dictionary_file_name="data_dictionary.csv"
        expected_url=f"s3://devplanetv1-mycommons-upload/{data_dict_guid}/{dictionary_file_name}"
        expected_json = {"file_name": dictionary_file_name, "dictionary_url": quote(expected_url)}

        mocked_indexd = MagicMock(requests.Response)
        mocked_indexd.status_code = 200
        mocked_indexd.json.return_value = {
            "acl":[],
            "authz":["/programs/DEV"],
            "did":data_dict_guid,
            "urls":[expected_url]
        }
        mocked_fence = MagicMock(requests.Response)
        mocked_fence.status_code = 200
        mocked_fence.json.return_value = {
            "url": expected_url
        }
        mocked_request.side_effect = [mocked_indexd, mocked_fence]
        mocked_client_secret.return_value = {"client_id": "client_id", "client_secret": "client_secret"}
        mocked_client_token.return_value = "my_client_token"

        try:
            GetDictionaryUrl.main(options=args)
            with open(args.output, 'r') as fh:
                result_json = json.load(fh)
            assert json.dumps(result_json) == json.dumps(expected_json)
        finally:
            cleanup_files([args.output])


    @patch('requests.get')
    def test_get_dictionary_url_no_guid_no_index(self, mocked_request):

        args = self.get_mock_args()

        data_dict_guid = args.data_dict_guid

        mocked_indexd_guid_not_found = MagicMock(requests.Response)
        mocked_indexd_guid_not_found.status_code = 404
        mocked_indexd_guid_not_found.json.return_value = {
            "error": "no record found",
        }
        mocked_indexd_missing_urls = MagicMock(requests.Response)
        mocked_indexd_missing_urls.status_code = 200
        mocked_indexd_missing_urls.json.return_value = {
            "acl":[],
            "authz":["/programs/DEV"],
            "did":data_dict_guid,
        }
        mocked_request.side_effect = [mocked_indexd_guid_not_found, mocked_indexd_missing_urls]

        expected_error = f"Data guid {args.data_dict_guid} not found in indexd"
        with pytest.raises(ValueError, match=expected_error):
            GetDictionaryUrl.main(options=args)
        assert os.path.exists(args.output) == False

        expected_error = f"File urls missing for guid {args.data_dict_guid} in indexd"
        with pytest.raises(ValueError, match=expected_error):
            GetDictionaryUrl.main(options=args)
        assert os.path.exists(args.output) == False


    @patch('requests.get')
    @patch('kubernetes.client.CoreV1Api.read_namespaced_secret')
    def test_get_dictionary_url_no_secrets(self, mocked_kube_client, mocked_indexd_request):

        args = self.get_mock_args()

        data_dict_guid = args.data_dict_guid
        dictionary_file_name="data_dictionary.csv"
        expected_url=f"s3://devplanetv1-mycommons-upload/{data_dict_guid}/{dictionary_file_name}"

        mocked_indexd_response = MagicMock(requests.Response)
        mocked_indexd_response.status_code = 200
        mocked_indexd_response.json.return_value = {
            "acl":[],
            "authz":["/programs/DEV"],
            "did":data_dict_guid,
            "urls":[expected_url]
        }
        mocked_indexd_request.return_value = mocked_indexd_response
        mocked_kube_client.side_effect = Exception("Mocked kube error")

        expected_error = f"Kubernetes could not read client secret"
        with pytest.raises(Exception, match=expected_error):
            GetDictionaryUrl.main(options=args)
        assert os.path.exists(args.output) == False


    @patch('requests.get')
    @patch('vlmd_submission_tools.common.utils.get_client_secret')
    @patch('vlmd_submission_tools.common.utils.get_client_token')
    def test_get_dictionary_url_bad_fence_response(self, mocked_client_token, mocked_client_secret, mocked_request):

        args = self.get_mock_args()

        data_dict_guid = args.data_dict_guid
        dictionary_file_name="data_dictionary.csv"
        expected_url=f"s3://devplanetv1-mycommons-upload/{data_dict_guid}/{dictionary_file_name}"

        mocked_indexd = MagicMock(requests.Response)
        mocked_indexd.status_code = 200
        mocked_indexd.json.return_value = {
            "acl":[],
            "authz":["/programs/DEV"],
            "did":data_dict_guid,
            "urls":[expected_url]
        }
        mocked_fence = MagicMock(requests.Response)
        mocked_fence.status_code = 404
        mocked_fence.json.return_value = {
            "message": "Not found"
        }
        mocked_request.side_effect = [mocked_indexd, mocked_fence]
        mocked_client_secret.return_value = {"client_id": "client_id", "client_secret": "client_secret"}
        mocked_client_token.return_value = "my_client_token"

        expected_error = "Could not get pre-signed url from fence"
        with pytest.raises(Exception, match=expected_error):
            GetDictionaryUrl.main(options=args)
        assert os.path.exists(args.output) == False
