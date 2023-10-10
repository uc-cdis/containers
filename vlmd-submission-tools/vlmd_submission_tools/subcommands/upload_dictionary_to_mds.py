"""Uploads the data dictionary to MDS.

@author: George Thomas <george42@uchicago.edu>,
         J Montgomery Maxwell <jmontmaxwell@uchicago.edu>,
         Michael Kranz <kranz-michael@norc.org>
"""

from argparse import ArgumentParser, Namespace
import json
import requests
import uuid

from vlmd_submission_tools.common import config
from vlmd_submission_tools.common.logger import Logger
from vlmd_submission_tools.subcommands import Subcommand
from vlmd_submission_tools.common import utils


class UploadDictionaryToMds(Subcommand):
    @classmethod
    def __add_arguments__(cls, parser: ArgumentParser) -> None:
        """Add the subcommand params"""

        parser.add_argument(
            "-j",
            "--json_local_path",
            required=True,
            type=str,
            help=(
                "Full path to the local json dictionary saved in the validation step, eg /mnt/vol/dict.json."
            ),
        )

        parser.add_argument(
            "-n",
            "--dictionary_name",
            required=True,
            type=str,
            help=(
                "The human readable name for the data dictionary, eg 'baseline' or 'follow up'."
            ),
        )

        parser.add_argument(
            "-s",
            "--study_id",
            required=True,
            type=str,
            help=(
                "The MDS study id associated with the data set."
            ),
        )

        parser.add_argument(
            "-o",
            "--output",
            required=True,
            type=str,
            help=(
                "Path to write out the JSON response with upload_status."
            ),
        )


    @classmethod
    def __get_description__(cls) -> str:
        """
        Description of tool.
        """
        return (
            "Takes a dictionary, the dictionary name and a study id. "
            "Adds the dictionary to the study id metadata."
            "Writes JSON output with the MDS upload_status."
        )

    @classmethod
    def main(cls, options: Namespace) -> None:
        """
        Entrypoint for UploadDictionaryToMds
        """
        logger = Logger.get_logger(cls.__tool_name__())
        logger.info(cls.__get_description__())

        # Read json dictionary from local path
        logger.info("Reading dictionary from local file system.")
        try:
            with open(options.json_local_path, "r") as fh:
                data_dictionary = json.load(fh)
        except:
            raise Exception("Could not read local json dictionary.")

        # verify that the submitted study-id exists in mds db
        logger.info(f"Checking for study ID {options.study_id} in MDS")
        existing_data_dictionaries = utils.check_mds_study_id(options.study_id, config.HOST_NAME)

        # test the client token - maybe put this in a try statement.
        # get token for mds api call
        logger.info("Getting client token")
        client_id, client_secret = utils.get_client_secret()
        token = utils.get_client_token(
            hostname = config.HOST_NAME,
            client_id = client_id,
            client_secret = client_secret)

        # upload the VLMD dictionary data to mds
        logger.info("Uploading dictionary to MDS")
        try:
            guid = str(uuid.uuid4())
            data = { "_guid_type": "data_dictionary",
                    "data_dictionary": data_dictionary['data_dictionary']}
            url = f"https://{config.HOST_NAME}/mds/metadata/{guid}"
            headers = {"Authorization": "bearer " + token, "content-type": "application/json"}
            response = requests.post(url, headers=headers, json=data)

            logger.info(f"Upload status code = {response.status_code}")
            logger.info(f"new guid={guid}")
            response.raise_for_status()
        except:
            raise Exception("Could not post dictionary to metadata")

        # check status of MDS response
        if response.status_code != 200 and response.status_code != 201:
            logger.error("Error in uploading dictionary to MDS")

        # add this name and guid to the study ID metadata
        logger.info(f"Adding dictionary_name '{options.dictionary_name}' to study ID = {options.study_id}")

        try:
            existing_data_dictionaries[options.dictionary_name] = f"{guid}"
            data = {"data_dictionaries": existing_data_dictionaries}
            url = f"https://{config.HOST_NAME}/mds/metadata/{options.study_id}?merge=True"
            response = requests.put(url, headers=headers, json=data)
            response.raise_for_status()
            logger.info("Success")
        except:
            logger.error("Error in updating study ID")
            raise Exception("Could not update data_dictionaries in study ID metadata")

        upload_status = "ok"
        logger.info(f"MDS upload status={upload_status}")

        # save the upload_status, dictionary_name and MDS guid output parameters
        record_json = {
            "upload_status": upload_status,
            "dictionary_name": options.dictionary_name,
            "mds_guid": guid
            }
        with open(options.output, 'w', encoding='utf-8') as o:
            json.dump(record_json, o, ensure_ascii=False, indent=4)
        logger.info(f"JSON response saved in {options.output}")
