"""Interacts with fence service to retrieve a presigned url for the data dictionary.

@author: George Thomas <george42@uchicago.edu>,
         J Montgomery Maxwell <jmontmaxwell@uchicago.edu>,
         Michael Kranz <kranz-michael@norc.org>
"""

from argparse import ArgumentParser, Namespace
import os
import requests

from vlmd_submission_tools.common import config
from vlmd_submission_tools.common.logger import Logger
from vlmd_submission_tools.common import utils
from vlmd_submission_tools.subcommands import Subcommand


class GetDictionaryUrl(Subcommand):
    @classmethod
    def __add_arguments__(cls, parser: ArgumentParser) -> None:
        """Add the subcommand params"""

        parser.add_argument(
            "-d",
            "--data_dict_guid",
            required=True,
            type=str,
            help=(
                "The indexd Globally Unique Identifier (GUID) for the data dictionary."
            ),
        )

    @classmethod
    def __get_description__(cls) -> str:
        """
        Description of tool.
        """
        return (
            "Takes an indexd guid and checks that the guid exists in indexd. "
            "Queries fence to get a presigned url for the data dictionary. "
            "Requires fence credentials: either user or client credentials."
        )

    @classmethod
    def main(cls, options: Namespace) -> None:
        """
        Entrypoint for CreateIndexdRecord
        """
        logger = Logger.get_logger(cls.__tool_name__())
        logger.info(cls.__get_description__())

        # config.HOST_NAME="qa-heal.planx-pla.net"
        # data_dict_guid="852b5e42-eb24-49a9-baa8-d565fd1b0b8b"
        logger.info(f"Searching indexd for guid.")
        try:
            url = f"https://{config.HOST_NAME}/index/index/{options.data_dict_guid}"
            response = requests.get(url)
        except:
            raise Exception(f"Could not get indexd data for data guid: {options.data_dict_guid}")
        logger.info(f"Indexd query status code = {response.status_code}")
        if response.status_code != 200:
            raise ValueError(f"Data guid {options.data_dict_guid} not found in indexd")

        indexd_urls = response.json().get("urls", None)
        if indexd_urls:
            file_name = os.path.basename(indexd_urls[0])
            logger.info(f"Dictionary file name: {file_name}")
        else:
            raise ValueError(f"File urls missing for guid {options.data_dict_guid} in indexd")

        logger.info("Getting fence client token")
        client_id, client_secret = utils.get_client_secret()
        logger.info("Using secret to get token")
        token = utils.get_client_token(
            hostname = config.HOST_NAME,
            client_id = client_id,
            client_secret = client_secret)

        logger.info("Got fence client token")

        logger.info(f"Querying fence for pre-signed url")
        try:
            url = f"https://{config.HOST_NAME}/user/data/download/{options.data_dict_guid}?protocol=s3"
            headers = {"Authorization": "bearer " + token, "content-type": "application/json"}
            response = requests.get(url, headers=headers)
            logger.info(f"Fence query status code = {response.status_code}")
            dictionary_url = response.json().get("url", None)
            logger.info(f"Dictionary url: {dictionary_url}")

        except:
            raise Exception("Could not get pre-signed url from fence")

        # return file_name and pre-signed url
        return (file_name, dictionary_url)
