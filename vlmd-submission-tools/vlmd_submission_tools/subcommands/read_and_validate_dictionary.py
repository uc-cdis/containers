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

from frictionless import Resource
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
            "-l",
            "--local_file_path",
            required=False,
            type=str,
            help=(
                "Local path for storing the json dictionary, eg /mnt/vol."
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

    @classmethod
    def __get_description__(cls) -> str:
        """
        Description of tool.
        """
        return (
            "Takes a presigned url and fetches the data dictionary. "
            "Converts any csv/tsv to json. "
            "Validates the dictionary against the provided schema. "
            "Returns True or False for valid dictionary."
        )

    @classmethod
    def main(cls, options: Namespace) -> None:
        """
        Entrypoint for ReadAndValidateDictionary
        """
        logger = Logger.get_logger(cls.__tool_name__())
        logger.info(cls.__get_description__())

        logger.info(f"URL {options.dictionary_url}")

        # Get file type from filename
        if options.file_name.lower().endswith('.json'):
            file_type = 'json'
        elif options.file_name.lower().endswith('.csv'):
            file_type = 'csv'
        elif options.file_name.lower().endswith('.tsv'):
            file_type = 'tsv'
        else:
            raise Exception("Could not get file type suffix from filename")
        local_file_path = f"{options.local_file_path}/{options.file_name}"

        # Pull in schema
        schema = schemas.heal['data_dictionary']
        data_dictionary_props = schema['properties']
        data_dictionary = {"title": "dictionary title"}
        mappings = mapping_utils.fieldmap

        logger.info(f"Fetching dictionary from s3 url.")
        if file_type == 'csv' or file_type == 'tsv':
            try:
                source = Resource(options.dictionary_url).to_petl()
            except:
                is_valid_dictionary = False
                traceback.print_exc()
                raise Exception(f"Could not read dictionary from url {options.dictionary_url}")

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

            try:
                data_dictionary['data_dictionary'] = [mapping_utils.convert_rec_to_json(rec) for rec in etl.dicts(template_tbl)]
                json_local_path = os.path.splitext(local_file_path)[0] + '.json'
            except:
                is_valid_dictionary = False
                traceback.print_exc()
                raise Exception(f"Could not convert {file_type} to json")
        else:
            # JSON format is read directly without conversion
            try:
                response = requests.get(options.dictionary_url)
                data_dictionary_json = response.text
                data_dictionary_json = json.loads(data_dictionary_json)
                data_dictionary['data_dictionary'] = data_dictionary_json
                json_local_path = local_file_path
            except:
                is_valid_dictionary = False
                traceback.print_exc()
                raise Exception(f"Could not read dictionary from url {options.dictionary_url}")

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

        # Save locally or as output artifact
        with open(json_local_path, 'w', encoding='utf-8') as o:
            json.dump(data_dictionary, o, ensure_ascii=False, indent=4)
        logger.info(f"JSON response saved in {json_local_path}")

        logger.info(f"json_local_path={json_local_path}")
        logger.info(f"Valid={is_valid_dictionary}")
        return (json_local_path, is_valid_dictionary)
