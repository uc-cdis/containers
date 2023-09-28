"""Tests for the ``vlmd_submission_tools.subcommands.ReadAndValidateDictionary`` subcommand"""
import os
from typing import NamedTuple
from unittest.mock import MagicMock, patch

from frictionless import FrictionlessException
import json
from parameterized import parameterized
from pathlib import Path
import pytest
import requests



from vlmd_submission_tools.subcommands import ReadAndValidateDictionary
from utils import cleanup_files

class MockArgs(NamedTuple):
    file_name: str
    json_local_path: str
    dictionary_url: str
    output: str


class TestReadAndValidateDictionarySubcommand:


    def get_mock_args(self, file_name, dictionary_url):
        return MockArgs(
            file_name=file_name,
            json_local_path="test_dictionary.json",
            dictionary_url=dictionary_url,
            output="validate.json",
        )


    @parameterized.expand(["json", "csv", "tsv"])
    def test_get_file_type_from_filename(self, suffix):
        filename=f"test.{suffix}"
        expected=suffix
        result = ReadAndValidateDictionary._get_file_type_from_filename(filename)
        assert result == expected


    def test_get_file_type_from_filename_exception(self):
        bad_filename="test.foo"
        expected_error="Could not get file type suffix from filename"
        with pytest.raises(Exception, match=expected_error):
            ReadAndValidateDictionary._get_file_type_from_filename(bad_filename)


    @parameterized.expand(["csv", "tsv"])
    def test_read_and_validate_dictionary_csv(self, suffix):
        # read valid csv/tsv dictionaries directly from file
        args = self.get_mock_args(f"template_submission.{suffix}",f"tests/templates/template_submission.{suffix}")
        expected_json = {
            "json_local_path": args.json_local_path,
            "is_valid_dictionary": True
        }

        try:
            ReadAndValidateDictionary.main(options=args)

            # The converted json dictionary
            assert Path(args.json_local_path).resolve().is_file()
            with open(args.json_local_path, 'r') as fh:
                converted_json = json.load(fh)
            assert "title" in converted_json
            assert "data_dictionary" in converted_json

            # The output json for subcommand
            with open(args.output, 'r') as fh:
                result_json = json.load(fh)
            assert json.dumps(result_json) == json.dumps(expected_json)
        finally:
            cleanup_files([args.json_local_path, args.output])


    @parameterized.expand(["csv"])
    def test_read_and_validate_dictionary_csv_invalid_dictionary(self, suffix):
        # read valid csv/tsv dictionaries directly from file
        args = self.get_mock_args(f"template_submission_bad_format.{suffix}",f"tests/templates/template_submission_bad_format.{suffix}")

        # Exception from bad input file
        expected_error="Not a valid dictionary"
        with pytest.raises(Exception, match=expected_error):
            ReadAndValidateDictionary.main(args)
        assert os.path.exists(args.output) == False


    @parameterized.expand(["csv", "tsv"])
    def test_read_and_validate_dictionary_csv_does_not_exist(self, suffix):
        # read valid csv/tsv dictionaries directly from file
        args = self.get_mock_args(f"dict_does_not_exist.{suffix}",f"tests/templates/dict_does_not_exist.{suffix}")

        try:
            # Exception from bad input file
            expected_error=f"Frictionless could not read dictionary from url {args.dictionary_url}"
            with pytest.raises(FrictionlessException, match=expected_error):
                ReadAndValidateDictionary.main(args)
            assert os.path.exists(args.json_local_path) == False
            assert os.path.exists(args.output) == False

        finally:
            cleanup_files([args.json_local_path, args.output])


    # JSON test will need mock of requests.get so that is reads the file from disk.
    @patch('requests.get')
    def test_read_and_validate_dictionary_json(self, mocked_request):
        # read valid json dictionary
        json_file_name = "template_submission_minimal.json"
        path_to_input_dict = f"tests/templates/{json_file_name}"
        args = self.get_mock_args(json_file_name,path_to_input_dict)
        expected_json = {
            "json_local_path": args.json_local_path,
            "is_valid_dictionary": True
        }
        # mock pre-signed url response by reading from local test file
        with open(path_to_input_dict, 'r') as fh:
            input_dict_json = json.load(fh)
        mocked_request.return_value.text = json.dumps(input_dict_json)

        try:
            ReadAndValidateDictionary.main(options=args)

            # when input dict is json then converted json is the same.
            assert Path(args.json_local_path).resolve().is_file()
            with open(args.json_local_path, 'r') as fh:
                converted_json = json.load(fh)
            assert "title" in converted_json
            assert "data_dictionary" in converted_json
            assert json.dumps(converted_json) == json.dumps(input_dict_json)

            # The output json for subcommand
            with open(args.output, 'r') as fh:
                result_json = json.load(fh)
            assert json.dumps(result_json) == json.dumps(expected_json)
        finally:
            cleanup_files([args.json_local_path, args.output])


    @patch('requests.get')
    def test_read_and_validate_dictionary_json_does_not_exist(self, mocked_request):
        # read valid csv/tsv dictionaries directly from file
        args = self.get_mock_args(f"dict_does_not_exist.json",f"https://tests/templates/dict_does_not_exist.json")

        # pre-signed url returns 404
        mocked_response = MagicMock(requests.Response)
        mocked_response.status_code = 404
        mocked_response.json.return_value = {
            "error": "no record found",
        }
        mocked_request.return_value = mocked_response
        mocked_request.return_value.text = "404 file not found"

        # Exception from bad input file
        expected_error=f"Could not read dictionary from url {args.dictionary_url}"
        with pytest.raises(Exception, match=expected_error):
            ReadAndValidateDictionary.main(args)
        assert os.path.exists(args.json_local_path) == False
        assert os.path.exists(args.output) == False
