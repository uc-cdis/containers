"""Tests for the ``vlmd_submission_tools.subcommands.ReadAndValidateDictionary`` subcommand"""
import os
import re
from typing import NamedTuple
from unittest import mock
from unittest.mock import MagicMock, patch

import json
from heal.vlmd.file_utils import get_output_filepath
from pathlib import Path
import pytest
import requests
import requests_mock

from vlmd_submission_tools.subcommands import ReadAndValidateDictionary
from utils import cleanup_files

DIR = Path(__file__).resolve().parent

class MockArgs(NamedTuple):
    file_name: str
    json_output_dir: str
    title: str
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

    def get_mock_args(self, file_name, json_output_dir, dictionary_url, output, title=None):
        return MockArgs(
            file_name=file_name,
            json_output_dir=json_output_dir,
            dictionary_url=dictionary_url,
            output=output,
            title=title,
        )


    @pytest.mark.parametrize("suffix", ["csv", "tsv", "json"])
    def test_get_file_type_from_filename(self, suffix):
        """Get the file suffix from the file name"""
        filename=f"test.{suffix}"
        expected=suffix
        result = ReadAndValidateDictionary._get_file_type_from_filename(filename)
        assert result == expected


    def test_get_file_type_from_filename_exception(self):
        """Test file name with unallowed suffix"""
        bad_filename="test.foo"
        expected_error="Could not get file type suffix from filename"
        with pytest.raises(Exception, match=expected_error):
            ReadAndValidateDictionary._get_file_type_from_filename(bad_filename)

    @pytest.mark.parametrize(
        "file_type, template_data",
        [
            ("csv", "template_submission_csv"),
            ("tsv", "template_submission_tsv"),
            ("json", "template_submission_json")
        ]
    )
    def test_download_from_url(
            self,
            file_type,
            template_data,
            download_dir,
            request
    ):
        """Test that downloaded data is saved locally"""

        url = "https://some.url"
        template_data = request.getfixturevalue(template_data)
        download_local_path = f"{download_dir}/test_dict.{file_type}"

        # mock requests to return the template-data fixture
        with requests_mock.Mocker() as m:

            if file_type == "json":
                m.get(url, json=template_data)
            else:
                m.get(
                    url,
                    content = bytes(template_data, 'utf-8')
                )

            result = ReadAndValidateDictionary._download_from_url(
                file_type, url, download_local_path
            )

            assert result == download_local_path
            assert os.path.exists(download_local_path)
            if file_type == "json":
                with open(download_local_path, 'r') as json_file:
                    downloaded_data = json.load(json_file)
            else:
                with open(download_local_path, 'r') as csv_file:
                     downloaded_data = csv_file.read()
            # saved data matches return from requests
            assert downloaded_data == template_data


    def test_download_from_url_failures(self, download_dir):
        """Test bad url and missing download directory"""

        file_type = "json"
        url = "https://some.url"
        json_local_path = get_output_filepath(
            download_dir, "test_file.csv", output_type="json"
        )
        csv_local_path = json_local_path.replace('json', 'csv')
        if os.path.exists(json_local_path):
            Path(json_local_path).unlink()

        with requests_mock.Mocker() as m:
            # bad url - request throws exception
            output_path = None
            m.get(url, exc=requests.HTTPError('Mocked HTTP Error'))
            expected_error="Mocked HTTP Error"

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
        """read valid json dictionary, validate, save report"""
        json_file_name = "template_submission_small.json"
        path_to_input_dict = f"tests/templates/{json_file_name}"
        args = self.get_mock_args(
            file_name=json_file_name,
            json_output_dir=download_dir,
            dictionary_url="https://some.url",
            output=f"{download_dir}/validate_artifact.json",
        )
        expected_json_local_path = f"{args.json_output_dir}/{args.file_name}"
        expected_validation_report = {
            "json_local_path": expected_json_local_path,
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
                assert Path(expected_json_local_path).resolve().is_file()
                with open(expected_json_local_path, 'r') as json_file:
                    downloaded_json = json.load(json_file)
                assert "fields" in downloaded_json
                assert downloaded_json == template_submission_json

                # The output validation report json for subcommand
                with open(args.output, 'r') as json_file:
                    validation_report = json.load(json_file)
                assert validation_report == expected_validation_report
        finally:
            cleanup_files([expected_json_local_path, args.output])


    def test_read_and_validate_dictionary_bad_url(self, download_dir):
        """Test error handling and output report in read_and_validate with bad url."""
        args = self.get_mock_args(
            file_name="some_template.json",
            json_output_dir=download_dir,
            dictionary_url="https://some.url",
            output=f"{download_dir}/validate_artifact.json",
        )
        expected_json_local_path = f"{args.json_output_dir}/{args.file_name}"
        expected_validation_report = {
            "json_local_path": None,
            "is_valid_dictionary": False,
            "errors": [
                f"Could not read dictionary from url {args.dictionary_url}"
            ]
        }
        with requests_mock.Mocker() as m:
            m.get(
                args.dictionary_url,
                text="404 file not found",
                status_code = 404
            )

            ReadAndValidateDictionary.main(args)

            assert os.path.exists(expected_json_local_path) == False
            assert Path(args.output).resolve().is_file()
            with open(args.output, 'r') as output_file:
                validation_report = json.load(output_file)
            assert validation_report == expected_validation_report


    def test_read_and_validate_dictionary_bad_local_path(
        self, template_submission_json, download_dir
    ):
        """
        With a bad download_dir there is no downloaded json
        but there could be a validation report.
        """
        args = self.get_mock_args(
            file_name="some_template.json",
            json_output_dir="/does/not/exist",
            dictionary_url="https://some.url",
            output=f"{download_dir}/validate_artifact.json",
        )
        expected_validation_report = {
            "json_local_path": None,
            "is_valid_dictionary": False,
            "errors": [
                f"Could not read dictionary from url {args.dictionary_url}"
            ]
        }
        with requests_mock.Mocker() as m:
            m.get(
                args.dictionary_url,
                text=json.dumps(template_submission_json)
            )
            expected_json_local_path = f"{args.json_output_dir}/{args.file_name}"

            ReadAndValidateDictionary.main(args)

            assert os.path.exists(expected_json_local_path) == False
            assert Path(args.output).resolve().is_file()
            with open(args.output, 'r') as output_file:
                validation_report = json.load(output_file)
            assert validation_report == expected_validation_report


    def test_read_and_validate_dictionary_json_invalid_dictionary(
        self, template_submission_invalid_json, download_dir
    ):
        """With a bad json dictionary, the file is downloaded and marked as invalid in report."""
        args = self.get_mock_args(
            file_name="template_submission_invalid.json",
            json_output_dir=download_dir,
            dictionary_url="https://some.url",
            output=f"{download_dir}/validate_artifact.json",
        )
        expected_json_local_path = f"{download_dir}/{args.file_name}"
        expected_validation_report = {
            "json_local_path": expected_json_local_path,
            "is_valid_dictionary": False,
            "errors": [
                "'character' is not one of ['number', 'integer', 'string', 'any', 'boolean', 'date', 'datetime', 'time', 'year', 'yearmonth', 'duration', 'geopoint']"
            ]
        }

        try:
            with requests_mock.Mocker() as m:
                m.get(
                    args.dictionary_url,
                    text=json.dumps(template_submission_invalid_json)
                )

                ReadAndValidateDictionary.main(options=args)

                assert Path(expected_json_local_path).resolve().is_file()
                assert Path(args.output).resolve().is_file()
                with open(args.output, 'r') as fh:
                    validation_report = json.load(fh)
                assert validation_report == expected_validation_report
        finally:
            cleanup_files([expected_json_local_path, args.output])


    @pytest.mark.parametrize(
        "suffix, template_data",
        [
            ("csv", "template_submission_csv"),
            ("tsv", "template_submission_tsv"),
        ]
    )
    def test_read_and_validate_dictionary_csv(
        self,
        suffix,
        template_data,
        template_submission_json,
        download_dir,
        request
    ):
        """
        Read valid csv/tsv dictionaries.
        The converted dictionaries should match the template_submission_json fixture.
        """

        args = self.get_mock_args(
            file_name=f"template_submission.{suffix}",
            json_output_dir=download_dir,
            title="Some title",
            dictionary_url="https://some.url",
            output=f"{download_dir}/validate_artifact.json",
        )
        expected_json_local_path = get_output_filepath(
            download_dir, args.file_name, output_type="json"
        )
        expected_validation_report = {
            "json_local_path": expected_json_local_path,
            "is_valid_dictionary": True,
            "errors": []
        }
        expected_converted_json = template_submission_json
        template_data = request.getfixturevalue(template_data)
        try:
            with requests_mock.Mocker() as m:
                m.get(
                    args.dictionary_url,
                    content = bytes(template_data, 'utf-8')
                )

                ReadAndValidateDictionary.main(options=args)

                # check for unconverted input data
                expected_local_path = f"{args.json_output_dir}/{args.file_name}"
                assert Path(expected_local_path).resolve().is_file()
                # check for converted json dictionary
                assert Path(expected_json_local_path).resolve().is_file()
                with open(expected_json_local_path, 'r') as f:
                    converted_json = json.load(f)
                assert converted_json.get('fields') == expected_converted_json.get('fields')
                # output validation report json artifact
                with open(args.output, 'r') as output_file:
                    validation_report = json.load(output_file)
                assert validation_report == expected_validation_report

        finally:
            cleanup_files([expected_local_path, expected_json_local_path, args.output])


    @pytest.mark.parametrize(
        "suffix, template_data",
        [
            ("csv", "template_submission_invalid_csv"),
            ("tsv", "template_submission_invalid_tsv"),
        ]
    )
    def test_read_and_validate_dictionary_csv_invalid_dictionary(
        self,
        suffix,
        template_data,
        download_dir,
        request
    ):
        """Invalid csv will get downloaded but not coverted."""
        args = self.get_mock_args(
            file_name=f"template_submission_invalid.{suffix}",
            json_output_dir=download_dir,
            dictionary_url="https://some.url",
            output=f"{download_dir}/validate_artifact.json",
            title="Some title",
        )
        csv_local_path = f"{download_dir}/{args.file_name}"
        expected_json_local_path = get_output_filepath(
            download_dir, args.file_name, output_type="json"
        )
        expected_validation_report = {
            "json_local_path": expected_json_local_path,
            "is_valid_dictionary": False,
            "errors": ["'name' is a required property"]
        }
        template_data = request.getfixturevalue(template_data)
        try:
            with requests_mock.Mocker() as m:
                m.get(
                    args.dictionary_url,
                    content=bytes(template_data, 'utf-8')
                )

                ReadAndValidateDictionary.main(options=args)

                assert Path(csv_local_path).resolve().is_file()
                # invalid csv input will not generate json output
                assert not Path(expected_json_local_path).resolve().is_file()
                # validation report should show errors
                assert Path(args.output).resolve().is_file()
                with open(args.output, 'r') as output_file:
                    validation_report = json.load(output_file)
                print(f"Validation report {validation_report}")
                assert validation_report == expected_validation_report

        finally:
            cleanup_files([csv_local_path, expected_json_local_path, args.output])
