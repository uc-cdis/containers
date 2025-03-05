"""Validates the data dictionary against the HEAL schema."""

from argparse import ArgumentParser, Namespace
import json
import os
from shutil import copyfile
import traceback
from urllib.parse import unquote

import requests
from heal.vlmd.extract.conversion import convert_to_vlmd
from heal.vlmd.extract.extract import vlmd_extract
from heal.vlmd.file_utils import get_output_filepath
from heal.vlmd.validate.json_validator import vlmd_validate_json
from heal.vlmd.validate.validate import vlmd_validate


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
                "Full path for saving the json dictionary, eg /mnt/vol/converted_dict.json."
            ),
        )

        parser.add_argument(
            "-t",
            "--title",
            required=False,
            default=None,
            type=str,
            help=(
                "Title for the dictionary (required for CSV input), eg 'Baseline VLMD for study'."
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
                "Path to write task output (with 'is_valid_dictionary')."
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

        input_file_name = options.file_name
        title = options.title

        json_local_path = options.json_local_path
        json_output_dir = os.path.dirname(os.path.abspath(json_local_path))
        input_dict_path = os.path.join(json_output_dir, input_file_name)
        if not os.path.isdir(os.path.dirname(json_output_dir)):
            logger.warning(f"Invalid directory for json_local_path: '{json_local_path}'.")
        if not os.path.isdir(os.path.dirname(os.path.abspath(options.output))):
            logger.warning(f"Invalid directory for artifact output: '{options.output}'.")

        file_type = cls._get_file_type_from_filename(input_file_name)
        local_path = None
        is_valid_dictionary = False
        validation_error = None
        errors_list = []
        report_json = {
            "json_local_path": None,
            "is_valid_dictionary": is_valid_dictionary,
            "errors": errors_list
        }

        # download from url and save local copy
        try:
            local_path = cls._download_from_url(file_type, dictionary_url, input_dict_path)
            if local_path:
                logger.info(f"Input dictionary saved in {local_path}")
            else:
                logger.warning("Input file not downloaded")

        except Exception as err:
            error_message = f"Could not read dictionary from url {dictionary_url}"
            logger.error(error_message)
            logger.error(err)

            report_json["errors"] = [error_message]
            with open(options.output, 'w', encoding='utf-8') as output_file:
                json.dump(report_json, output_file, ensure_ascii=False, indent=4)
            logger.info(f"Validation report saved in {options.output}")
            return

        logger.info(f"Getting validation report for {local_path}")

        if file_type == 'json':
            try:
                # just validate, don't convert
                is_valid_dictionary = vlmd_validate(
                    local_path,
                    file_type=file_type,
                    output_type="json",
                    return_converted_output=False,
                )
                converted_json_path = local_path

            except Exception as err:
                validation_error = str(err)
                # TODO: remove this parsing after the heal-sdk has trimmed down the error size.
                validation_error = validation_error.split('\n')[0]
                logger.error(f"Error in json validation: {err}")

        if file_type == 'csv' or file_type == 'tsv':
            logger.info(f"Converting {file_type} to JSON")
            if title is None:
                logger.warning("Missing 'title' parameter. Will check for standardsMappings")

            try:
                converted_json_path = get_output_filepath(
                    json_output_dir, input_file_name, output_type="json"
                )
                # use file_type="auto" so we can handle csv, tsv, REDCap
                is_valid_dictionary = vlmd_extract(
                    input_file=local_path,
                    title=title,
                    file_type="auto",
                    output_dir=json_output_dir,
                    output_type="json"
                )

                if os.path.exists(converted_json_path):
                    logger.info(f"Converted JSON data dictionary saved in {converted_json_path}")
                else:
                    logger.warning(f"Not finding converted file in {converted_json_path}")
            except Exception as err:
                logger.error(f"Error in validating and extracting dictionary from {local_path}")
                logger.error(f"Error type {type(err).__name__}")
                validation_error = str(err)
                # TODO: remove this line if heal-sdk becomes less verbose
                validation_error = validation_error.split('\n')[0]
                logger.error(validation_error)

        logger.info(f"Valid json dictionary = {is_valid_dictionary}")
        logger.info(f"Validation errors = {validation_error}")
        if validation_error:
            errors_list.append(validation_error)

        # copy converted json file written by extract into path specified in workflow
        if is_valid_dictionary:
            try:
                if json_local_path != converted_json_path:
                    copyfile(converted_json_path, json_local_path)
            except Exception as err:
                error_message = "Could not copy extracted file to 'json_local_path'"
                logger.error(error_message)
                logger.error(err)

        report_json = {
            "json_local_path": json_local_path,
            "is_valid_dictionary": is_valid_dictionary,
            "errors": errors_list
        }
        # save the validation report artifact
        with open(options.output, 'w', encoding='utf-8') as output_file:
            json.dump(report_json, output_file, ensure_ascii=False, indent=4)
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
                with open(json_local_path, 'w', encoding='utf-8') as json_file:
                    json.dump(data_dictionary, json_file, ensure_ascii=False, indent=4)
                return json_local_path
            elif file_type == 'csv' or file_type == 'tsv':
                data_dictionary = response.content
                csv_local_path = json_local_path.replace('json', f"{file_type}")
                with open(csv_local_path, 'wb') as csv_file:
                    csv_file.write(data_dictionary)
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
