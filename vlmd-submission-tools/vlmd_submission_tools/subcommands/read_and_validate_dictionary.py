"""Validates the data dictionary against the HEAL schema.

@author: George Thomas <george42@uchicago.edu>,
         J Montgomery Maxwell <jmontmaxwell@uchicago.edu>,
         Michael Kranz <kranz-michael@norc.org>
"""

from argparse import ArgumentParser, Namespace
import json
import jsonschema
import os
import traceback
from urllib.parse import unquote

from frictionless import Resource, FrictionlessException
import petl as etl
import requests

from vlmd_submission_tools.common.logger import Logger
from vlmd_submission_tools.common import config
from vlmd_submission_tools.common import mapping_utils
from vlmd_submission_tools.common import utils
from vlmd_submission_tools.common import schemas
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
            "Converts any csv/tsv to json and saves to local file system. "
            "Validates the dictionary against the provided schema. "
            "Writes JSON output with json_local_path and is_valid_dictionary."
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

        # pull in schema
        schema = schemas.heal['data_dictionary']
        data_dictionary_props = schema['properties']
        data_dictionary = {"title": "dictionary title"}
        mappings = mapping_utils.fieldmap

        logger.info(f"Fetching dictionary from s3 url.")
        if file_type == 'csv' or file_type == 'tsv':
            try:
                source = Resource(dictionary_url)
                source = source.to_petl()

                logger.info(f"Converting {file_type} file to json")
                logger.info(f"Column names in petl: {source.fieldnames()}")
                fields_to_add = [
                    (field,'')
                    for field in mappings.keys()
                    if not field in source.fieldnames()
                ]
                template_tbl = (
                    source
                    .addfields(fields_to_add) # add fields from mappings not in the csv template to allow convert fxns to work
                    .convert(mappings)
                    .convertnumbers()
                    .cut(source.fieldnames()) # want to include only fields in csv
                )
            except FrictionlessException:
                is_valid_dictionary = False
                traceback.print_exc()
                raise FrictionlessException(f"Frictionless could not read dictionary from url {dictionary_url}")
            except:
                is_valid_dictionary = False
                traceback.print_exc()
                raise Exception(f"Could not read dictionary from url {dictionary_url}")

            try:
                data_dictionary['data_dictionary'] = [mapping_utils.convert_rec_to_json(rec) for rec in etl.dicts(template_tbl)]
            except:
                is_valid_dictionary = False
                traceback.print_exc()
                raise Exception(f"Could not convert {file_type} to json")
        else:
            # JSON format is read directly without conversion
            try:
                response = requests.get(dictionary_url)
                data_dictionary_json = response.text
                data_dictionary = json.loads(data_dictionary_json)
            except:
                is_valid_dictionary = False
                traceback.print_exc()
                raise Exception(f"Could not read dictionary from url {dictionary_url}")

        logger.info("Reading schema into schema_array")
        schema_array = {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "$id": "vlmd",
            "title":"Variable Level Metadata (Data Dictionaries)",
            "description": "This schema defines the variable level metadata for one data dictionary for a given study.Note a given study can have multiple data dictionaries",
            "type": "array",
            "items": schema
        }

        logger.info("Validating dictionary.")
        is_valid_dictionary = True
        try:
            jsonschema.validate(data_dictionary['data_dictionary'],schema=schema_array)
        except:
            is_valid_dictionary = False
            traceback.print_exc()
            raise Exception("Not a valid dictionary")
        logger.info(f"Valid={is_valid_dictionary}")

        # save the data dictionary
        with open(json_local_path, 'w', encoding='utf-8') as o:
            json.dump(data_dictionary, o, ensure_ascii=False, indent=4)
        logger.info(f"JSON data dictionary saved in {json_local_path}")

        # save the json_local_path and is_valid_dictionary output parameters
        record_json = {"json_local_path": json_local_path, "is_valid_dictionary": is_valid_dictionary}
        with open(options.output, 'w', encoding='utf-8') as o:
            json.dump(record_json, o, ensure_ascii=False, indent=4)
        logger.info(f"JSON response saved in {options.output}")


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
