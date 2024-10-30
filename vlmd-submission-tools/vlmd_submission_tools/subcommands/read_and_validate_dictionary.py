"""Validates the data dictionary against the HEAL schema.

@author: George Thomas <george42@uchicago.edu>,
         J Montgomery Maxwell <jmontmaxwell@uchicago.edu>,
         Michael Kranz <kranz-michael@norc.org>
"""

from argparse import ArgumentParser, Namespace
import json
import traceback
from urllib.parse import unquote

import requests
from healdata_utils import validate_vlmd_csv, validate_vlmd_json
from healdata_utils.conversion import convert_to_vlmd

from vlmd_submission_tools.common.logger import Logger
from vlmd_submission_tools.subcommands import Subcommand


class ReadAndValidateDictionary(Subcommand):
    @classmethod
    def __add_arguments__(cls, parser: ArgumentParser) -> None:
        """Add the subcommand params"""

        parser.add_argument(
            "-f",
            "--file_name",
            required=True,
            type=str,
            help=(
                "The file name of the data dictionary submitted by the user."
            ),
        )

        parser.add_argument(
            "-j",
            "--json_local_path",
            required=True,
            type=str,
            help=(
                "Full path for saving the dictionary in json, eg /mnt/vol/dict.json."
            ),
        )

        parser.add_argument(
            "-u",
            "--dictionary_url",
            required=True,
            type=str,
            help=(
                "The pre-signed url for the data dictionary."
            ),
        )

        parser.add_argument(
            "-o",
            "--output",
            required=True,
            type=str,
            help=(
                "Path to write out the JSON response with json_local_path and is_valid_dictionary."
            ),
        )

    @classmethod
    def __get_description__(cls) -> str:
        """
        Description of tool.
        """
        return (
            "Takes a presigned url and fetches the data dictionary. "
            "Validates the dictionary against the healdata-utils schema. "
            "Writes JSON output with json_local_path and validation report. "
        )

    @classmethod
    def main(cls, options: Namespace) -> None:
        """
        Entrypoint for ReadAndValidateDictionary
        """
        logger = Logger.get_logger(cls.__tool_name__())
        logger.info(cls.__get_description__())

        dictionary_url = options.dictionary_url
        dictionary_url = unquote(dictionary_url)
        logger.info(f"URL {dictionary_url}")

        file_type = cls._get_file_type_from_filename(options.file_name)
        json_local_path = options.json_local_path
        local_path = None
        is_valid_dictionary = None
        errors_list = None

        # download from url and save local copy
        try:
            local_path = cls._download_from_url(file_type, dictionary_url, json_local_path)
            if local_path:
                logger.info(f"Data dictionary saved in {local_path}")

        except Exception as e:
            logger.error(f"Could not read dictionary from url {dictionary_url}")
            logger.error(e)
            logger.error(f"Exception type = {type(e)}")
            return

        # get validation report with healdata-utils.validate_vlmd
        logger.info(f"Getting validation report for {local_path}")
        try:
            if file_type == 'json':
                result = validate_vlmd_json(local_path)
            elif file_type == 'csv' or file_type == 'tsv':
                result = validate_vlmd_csv(local_path)
            validation_report = result.get('report')

            is_valid_dictionary = validation_report.get('valid')
            errors_list = validation_report.get('errors')
        except Exception as e:
            logger.error(f"Error in validation: {e}")

        logger.info(f"Valid dictionary = {is_valid_dictionary}")
        logger.info(f"Errors from validation report = {errors_list}")

        # convert csv to json for uploading to MDS.
        if file_type == 'csv' or file_type == 'tsv':
            logger.info(f"Converting {file_type} to JSON")
            props = {
                "description": f"Json dictionary converted from {file_type}",
                "title": "HEAL compliant variable level metadata dictionary"
            }

            vlmd_dict = convert_to_vlmd(
                input_filepath = local_path,
                data_dictionary_props = props,
                inputtype = "csv-data-dict",
            )
            converted_json = vlmd_dict.get('jsontemplate')

        # logger.info(f"Converted JSON is valid dictionary = convertis_valid_dictionary}")
        # logger.info(f"Errors from validation report = {errors_list}")
            logger.info(f"Errors = {vlmd_dict.get('errors')}")

            with open(json_local_path, 'w', encoding='utf-8') as o:
                json.dump(converted_json, o, ensure_ascii=False, indent=4)
            logger.info(f"Converted JSON data dictionary saved in {json_local_path}")


        report_json = {
            "json_local_path": json_local_path,
            "is_valid_dictionary": is_valid_dictionary,
            "errors": errors_list
        }
        # save the validation report artifact
        with open(options.output, 'w', encoding='utf-8') as o:
            json.dump(report_json, o, ensure_ascii=False, indent=4)
        logger.info(f"Validation report saved in {options.output}")


    @classmethod
    def _download_from_url(cls, file_type: str, url: str, json_local_path: str) -> str:
        """
        Sends a request to the url and saves data in the local_path

        Args:
            file_type (str): 'csv', 'tsv', 'json'
            url (str): the url for the data dictionary
            json_local_path (str): the path to the local copy, eg, '/tmp/vlmd/dict.json'

        Returns:
            path of saved contents, None if error in downloading.
        """
        local_path = None
        try:
            response = requests.get(url)
            data_dictionary = response.text
            if file_type == 'json':
                data_dictionary = response.text
                data_dictionary = json.loads(data_dictionary)
                with open(json_local_path, 'w', encoding='utf-8') as f:
                    json.dump(data_dictionary, f, ensure_ascii=False, indent=4)
                return json_local_path
            elif file_type == 'csv' or file_type == 'tsv':
                data_dictionary = response.content
                csv_local_path = json_local_path.replace('json', f"{file_type}")
                with open(csv_local_path, 'wb') as f:
                    f.write(data_dictionary)
                return csv_local_path
        except Exception as exc:
            raise(exc)

        return local_path


    @classmethod
    def _get_file_type_from_filename(cls, file_name: str):
        if file_name.lower().endswith('.json'):
            file_type = 'json'
        elif file_name.lower().endswith('.csv'):
            file_type = 'csv'
        elif file_name.lower().endswith('.tsv'):
            file_type = 'tsv'
        else:
            raise Exception("Could not get file type suffix from filename")

        return file_type
