"""Tests for the ``vlmd_submission_tools.subcommands.UploadDictionaryToMds`` subcommand"""
import os
from typing import NamedTuple
from unittest.mock import MagicMock, patch

import json
import pytest
import requests
import uuid

from utils import cleanup_files
from vlmd_submission_tools.subcommands import UploadDictionaryToMds


class MockArgs(NamedTuple):
    json_local_path: str
    dictionary_name: str
    study_id: str
    output: str


class TestGetDictionaryUrlSubcommand:

    def get_mock_args(self):
        return MockArgs(
            json_local_path="tests/templates/template_submission_minimal.json",
            dictionary_name="Minimal_json_dict",
            study_id="my_study_id",
            output="upload_output.json",
        )


    @patch('vlmd_submission_tools.common.utils.check_mds_study_id')
    @patch('vlmd_submission_tools.common.utils.get_client_secret')
    @patch('vlmd_submission_tools.common.utils.get_client_token')
    @patch('requests.post')
    @patch('requests.put')
    def test_upload_dictionary_to_mds(self, mocked_mds_put, mocked_mds_post, mocked_client_token, mocked_client_secret, mocked_check_mds):

        args = self.get_mock_args()
        existing_data_dictionaries = {
            "CVS baseline": "guid-1",
            "JSON followup": "guid-2"
        }
        mocked_check_mds.return_value = existing_data_dictionaries

        mocked_client_secret.return_value = {"client_id": "client_id", "client_secret": "client_secret"}
        mocked_client_token.return_value = "my_client_token"

        # read json dictionary from local file
        with open(args.json_local_path, 'r') as fh:
            json_dictionary = json.load(fh)
        mocked_post_response = MagicMock(requests.Response)
        mocked_post_response.status_code = 200
        mocked_post_response.json.return_value = {
            "_guid_type": "data_dictionary",
            "data_dictionary": json_dictionary
        }
        mocked_mds_post.return_value = mocked_post_response

        new_data_dictionaries = {
            "CVS baseline": "guid-1",
            "JSON followup": "guid-2",
            args.dictionary_name: "guid-3"
        }
        new_metadata = {
            "_guid_type": "discovery_metadata",
            "gen3_discovery": "discovery_metadata",
            "data_dictionaries": new_data_dictionaries
        }
        mocked_put_response = MagicMock(requests.Response)
        mocked_put_response.status_code = 200
        mocked_put_response.json.return_value = new_metadata
        mocked_mds_put.return_value = mocked_put_response

        try:
            UploadDictionaryToMds.main(options=args)
            with open(args.output, 'r') as fh:
                result_json = json.load(fh)
            assert result_json.get("upload_status") == "ok"
            assert result_json.get("dictionary_name") == args.dictionary_name
            try:
                uuid.UUID(result_json.get("mds_guid"))
                assert True
            except ValueError:
                assert False
        finally:
            cleanup_files([args.output])


    @patch('vlmd_submission_tools.common.utils.check_mds_study_id')
    @patch('vlmd_submission_tools.common.utils.get_client_secret')
    @patch('vlmd_submission_tools.common.utils.get_client_token')
    @patch('requests.post')
    def test_upload_dictionary_to_mds_failed_upload(self, mocked_mds_post, mocked_client_token, mocked_client_secret, mocked_check_mds):

        args = self.get_mock_args()
        existing_data_dictionaries = {
            "CVS baseline": "guid-1",
            "JSON followup": "guid-2"
        }
        mocked_check_mds.return_value = existing_data_dictionaries

        mocked_client_secret.return_value = {"client_id": "client_id", "client_secret": "client_secret"}
        mocked_client_token.return_value = "my_client_token"

        mocked_mds_post.side_effect = Exception("Mocked error")

        expected_error = "Could not post dictionary to metadata"
        with pytest.raises(Exception, match=expected_error):
            UploadDictionaryToMds.main(options=args)
        assert os.path.exists(args.output) == False


    @patch('vlmd_submission_tools.common.utils.check_mds_study_id')
    @patch('vlmd_submission_tools.common.utils.get_client_secret')
    @patch('vlmd_submission_tools.common.utils.get_client_token')
    @patch('requests.post')
    @patch('requests.put')
    def test_upload_dictionary_to_mds_failed_update(self, mocked_mds_put, mocked_mds_post, mocked_client_token, mocked_client_secret, mocked_check_mds):

        args = self.get_mock_args()
        existing_data_dictionaries = {
            "CVS baseline": "guid-1",
            "JSON followup": "guid-2"
        }
        mocked_check_mds.return_value = existing_data_dictionaries

        mocked_client_secret.return_value = {"client_id": "client_id", "client_secret": "client_secret"}
        mocked_client_token.return_value = "my_client_token"

        # read json dictionary from local file
        with open(args.json_local_path, 'r') as fh:
            json_dictionary = json.load(fh)
        mocked_post_response = MagicMock(requests.Response)
        mocked_post_response.status_code = 200
        mocked_post_response.json.return_value = {
            "_guid_type": "data_dictionary",
            "data_dictionary": json_dictionary
        }
        mocked_mds_post.return_value = mocked_post_response

        mocked_mds_put.side_effect = Exception("Mocked error")

        expected_error = "Could not update data_dictionaries in study ID metadata"
        with pytest.raises(Exception, match=expected_error):
            UploadDictionaryToMds.main(options=args)
        assert os.path.exists(args.output) == False
