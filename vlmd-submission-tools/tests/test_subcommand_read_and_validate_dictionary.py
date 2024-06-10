"""Tests for the ``vlmd_submission_tools.subcommands.ReadAndValidateDictionary`` subcommand"""
import os
import re
from typing import NamedTuple
from unittest import mock
from unittest.mock import MagicMock, patch

import json
from parameterized import parameterized
from pathlib import Path
import pytest
import requests
import requests_mock

from vlmd_submission_tools.subcommands import ReadAndValidateDictionary
from utils import cleanup_files

DIR = Path(__file__).resolve().parent

class MockArgs(NamedTuple):
    file_name: str
    json_local_path: str
    dictionary_url: str
    output: str


@pytest.fixture(scope="session")
def download_dir(tmpdir_factory):
    path = tmpdir_factory.mktemp("vlmd_download_dir")
    return path


@pytest.fixture
def template_submission_json():
    with open(Path(DIR, "templates/template_submission_small.json")) as f:
        return json.load(f)


@pytest.fixture
def template_submission_invalid_json():
    with open(Path(DIR, "templates/template_submission_invalid.json")) as f:
        return json.load(f)


@pytest.fixture
def template_submission_csv():
    with open(Path(DIR, "templates/template_submission_small.csv")) as f:
        # return re.escape(f.read())
        # return bytes(f.read(), 'utf-8')
        return f.read()


@pytest.fixture
def template_submission_invalid_csv():
    with open(Path(DIR, "templates/template_submission_invalid.csv")) as f:
        return f.read()


@pytest.fixture
def template_submission_tsv():
    with open(Path(DIR, "templates/template_submission_small.tsv")) as f:
        # return re.escape(f.read())
        # return bytes(f.read(), 'utf-8')
        return f.read()


@pytest.fixture
def template_submission_invalid_tsv():
    with open(Path(DIR, "templates/template_submission_invalid.tsv")) as f:
        return f.read()


class TestReadAndValidateDictionarySubcommand:

    def get_mock_args(self, file_name, json_local_path, dictionary_url, output):
        return MockArgs(
            file_name=file_name,
            json_local_path=json_local_path,
            dictionary_url=dictionary_url,
            output=output,
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


    def test_download_from_url(
            self,
            template_submission_json,
            template_submission_csv,
            template_submission_tsv,
            download_dir
    ):

        url = "https://some.url"
        json_local_path = f"{download_dir}/test_dict.json"
        with requests_mock.Mocker() as m:

            file_type = "json"
            # good data from url
            m.get(url, json=template_submission_json)
            result = ReadAndValidateDictionary._download_from_url(
                file_type, url, json_local_path
            )
            assert result == json_local_path
            assert os.path.exists(json_local_path)
            # TODO: read file and assert that is equal to mock_data
            with open(json_local_path, 'r') as f:
                    downloaded_json = json.load(f)
            assert downloaded_json == template_submission_json

            file_type = "csv"
            expected_local_path = json_local_path.replace('json', f"{file_type}")
            m.get(
                url,
                content = bytes(template_submission_csv, 'utf-8')
            )

            result = ReadAndValidateDictionary._download_from_url(
                file_type, url, json_local_path
            )
            assert result == expected_local_path
            assert os.path.exists(expected_local_path)
            with open(expected_local_path, 'r') as f:
                    downloaded_csv = f.read()
            assert downloaded_csv == template_submission_csv

            file_type = "tsv"
            expected_local_path = json_local_path.replace('json', f"{file_type}")
            m.get(
                url,
                content = bytes(template_submission_tsv, 'utf-8')
            )

            result = ReadAndValidateDictionary._download_from_url(
                file_type, url, json_local_path
            )
            assert result == expected_local_path
            assert os.path.exists(expected_local_path)
            with open(expected_local_path, 'r') as f:
                    downloaded_tsv = f.read()
            assert downloaded_tsv == template_submission_tsv


    def test_download_from_url_failures(self, download_dir):

        file_type = "json"
        url = "https://some.url"
        json_local_path = f"{download_dir}/test_dict.json"
        csv_local_path = json_local_path.replace('json', 'csv')
        if os.path.exists(json_local_path):
            Path(json_local_path).unlink()

        with requests_mock.Mocker() as m:
            # bad url - request throws exception
            output_path = None
            m.get(url, exc=requests.HTTPError('Mocked HTTP Error'))
            expected_error=f"Mocked HTTP Error"
            with pytest.raises(Exception, match=expected_error):
                output_path = ReadAndValidateDictionary._download_from_url(
                file_type, url, json_local_path
            )
            assert output_path == None
            assert os.path.exists(json_local_path) == False

            # have a good url but a bad json_local_path
            output_path = None
            bad_local_path = "/does/not/exist.json"
            csv_local_path = bad_local_path.replace('json', 'csv')
            mock_data = {"title": "test json data"}
            m.get(url, json=mock_data)
            expected_error = re.escape(f"[Errno 2] No such file or directory: '{bad_local_path}'")
            with pytest.raises(Exception, match=expected_error):
                output_path = ReadAndValidateDictionary._download_from_url(
                file_type, url, bad_local_path
            )
            # no output file, no converted json, no original csv
            assert output_path == None
            assert os.path.exists(json_local_path) == False
            assert os.path.exists(csv_local_path) == False


    def test_read_and_validate_dictionary_json(self, template_submission_json, download_dir):
        # read valid json dictionary
        json_file_name = "template_submission_small.json"
        path_to_input_dict = f"tests/templates/{json_file_name}"
        args = self.get_mock_args(
            file_name=json_file_name,
            json_local_path=f"{download_dir}/test_dictionary.json",
            dictionary_url="https://some.url",
            output=f"{download_dir}/validate_artifact.json",
        )
        expected_validation_report = {
            "json_local_path": args.json_local_path,
            "is_valid_dictionary": True,
            "errors": []
        }


        try:
            with requests_mock.Mocker() as m:
                m.get(
                    args.dictionary_url,
                    text=json.dumps(template_submission_json)
                )

                ReadAndValidateDictionary.main(options=args)

                # downloaded json dict is saved in 'json_local_path'.
                assert Path(args.json_local_path).resolve().is_file()
                with open(args.json_local_path, 'r') as fh:
                    downloaded_json = json.load(fh)
                assert "fields" in downloaded_json
                assert downloaded_json == template_submission_json

                # The output validation report json for subcommand
                with open(args.output, 'r') as fh:
                    validation_report = json.load(fh)
                assert validation_report == expected_validation_report
        finally:
            cleanup_files([args.json_local_path, args.output])


    def test_read_and_validate_dictionary_bad_url(self):
        args = self.get_mock_args(
            file_name="some_template.json",
            json_local_path=f"{download_dir}/test_dictionary.json",
            dictionary_url="https://some.url",
            output=f"{download_dir}/validate_artifact.json",
        )
        with requests_mock.Mocker() as m:
            m.get(
                args.dictionary_url,
                text="404 file not found",
                status_code = 404
            )

            ReadAndValidateDictionary.main(args)
            assert os.path.exists(args.json_local_path) == False
            assert os.path.exists(args.output) == False


    def test_read_and_validate_dictionary_bad_local_path(
        self, template_submission_json, download_dir
    ):
        args = self.get_mock_args(
            file_name="some_template.json",
            json_local_path="/does/not/exist",
            dictionary_url="https://some.url",
            output=f"{download_dir}/validate_artifact.json",
        )
        with requests_mock.Mocker() as m:
            m.get(
                args.dictionary_url,
                text=json.dumps(template_submission_json)
            )

            ReadAndValidateDictionary.main(args)
            assert os.path.exists(args.json_local_path) == False
            assert os.path.exists(args.output) == False


    def test_read_and_validate_dictionary_json_invalid_dictionary(
        self, template_submission_invalid_json, download_dir
    ):
        args = self.get_mock_args(
            file_name=f"template_submission_invalid.json",
            json_local_path=f"{download_dir}/test_dict.json",
            dictionary_url="https://some.url",
            output=f"{download_dir}/validate_artifact.json",
        )
        expected_validation_report = {
            "json_local_path": args.json_local_path,
            "is_valid_dictionary": False,
            "errors": [{
                'json_path': '$.fields[0].type',
                'message': "'character' is not one of ['number', 'integer', 'string', 'any', 'boolean', 'date', 'datetime', 'time', 'year', 'yearmonth', 'duration', 'geopoint']"
            }]
        }

        try:
            with requests_mock.Mocker() as m:
                m.get(
                    args.dictionary_url,
                    text=json.dumps(template_submission_invalid_json)
                )
                ReadAndValidateDictionary.main(options=args)
                # we should have our downloaded json file
                assert Path(args.json_local_path).resolve().is_file()
                # the validation report should show errors
                assert Path(args.output).resolve().is_file()
                with open(args.output, 'r') as fh:
                    validation_report = json.load(fh)
                assert validation_report == expected_validation_report
        finally:
            cleanup_files([args.json_local_path, args.output])


    @pytest.mark.parametrize(
        "suffix",
        ["csv", "tsv"]
    )
    def test_read_and_validate_dictionary_csv(
        self,
        template_submission_csv,
        template_submission_tsv,
        template_submission_json,
        download_dir,
        suffix
    ):

        args = self.get_mock_args(
            file_name=f"template_submission.{suffix}",
            json_local_path=f"{download_dir}/test_dictionary.json",
            dictionary_url="https://some.url",
            output=f"{download_dir}/validate_artifact.json",
        )
        expected_validation_report = {
            "json_local_path": args.json_local_path,
            "is_valid_dictionary": True,
            "errors": []
        }
        expected_converted_json = template_submission_json
        try:
            with requests_mock.Mocker() as m:

                if suffix == 'csv':
                    m.get(
                        args.dictionary_url,
                        content = bytes(template_submission_csv, 'utf-8')
                    )
                elif suffix == 'tsv':
                     m.get(
                        args.dictionary_url,
                        content = bytes(template_submission_tsv, 'utf-8')
                    )

                ReadAndValidateDictionary.main(options=args)

                # we should have a file for unconverted data
                expected_local_path = args.json_local_path.replace('json', f'{suffix}')
                assert Path(expected_local_path).resolve().is_file()
                # we should have a converted json dictionary
                assert Path(args.json_local_path).resolve().is_file()
                with open(args.json_local_path, 'r') as f:
                    converted_json = json.load(f)
                assert converted_json.get('fields') == expected_converted_json.get('fields')
                # output validation report json artifact
                with open(args.output, 'r') as f:
                    validation_report = json.load(f)
                assert validation_report == expected_validation_report

        finally:
            cleanup_files([expected_local_path, args.json_local_path, args.output])


    @pytest.mark.parametrize(
        "suffix",
        ["csv", "tsv"]
    )
    def test_read_and_validate_dictionary_csv_invalid_dictionary(
        self,
        template_submission_invalid_csv,
        template_submission_invalid_tsv,
        download_dir,
        suffix
    ):
        args = self.get_mock_args(
            file_name=f"template_submission_invalid.{suffix}",
            json_local_path=f"{download_dir}/test_dict.json",
            dictionary_url="https://some.url",
            output=f"{download_dir}/validate_artifact.json",
        )
        expected_validation_report = {
            "json_local_path": args.json_local_path,
            "is_valid_dictionary": False,
            "errors": [{
                'json_path': '$[0].type',
                'message': "'character' is not valid under any of the given schemas"
            }]
        }

        try:
            with requests_mock.Mocker() as m:
                if suffix == 'csv':
                    m.get(
                        args.dictionary_url,
                        content=bytes(template_submission_invalid_csv, 'utf-8')
                    )
                elif suffix == 'tsv':
                     m.get(
                        args.dictionary_url,
                        content=bytes(template_submission_invalid_tsv, 'utf-8')
                    )

                ReadAndValidateDictionary.main(options=args)

                # csv file should have been downloaded
                csv_local_path = args.json_local_path.replace('json',f'{suffix}')
                assert Path(csv_local_path).resolve().is_file()
                assert Path(args.json_local_path).resolve().is_file()
                # validation report should show errors
                assert Path(args.output).resolve().is_file()
                with open(args.output, 'r') as fh:
                    validation_report = json.load(fh)
                assert validation_report == expected_validation_report

        finally:
            cleanup_files([csv_local_path, args.json_local_path, args.output])
