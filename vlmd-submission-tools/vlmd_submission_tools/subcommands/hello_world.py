"""Placeholder method for testing argo workflows.
"""


from argparse import ArgumentParser, Namespace
import json

from vlmd_submission_tools.common.logger import Logger
from vlmd_submission_tools.subcommands import Subcommand


class HelloWorld(Subcommand):
    @classmethod
    def __add_arguments__(cls, parser: ArgumentParser) -> None:
        """Add the subcommand params"""

        parser.add_argument(
            "-f",
            "--from_flag",
            required=False,
            type=str,
            default="VLMD",
            help=(
                "Optional flag for testing in workflow."
            ),
        )
        parser.add_argument(
            "-o",
            "--output",
            required=True,
            type=str,
            help=(
                "Path to write out the JSON response, the hello-world message."
            ),
        )

    @classmethod
    def __get_description__(cls) -> str:
        """
        Description of tool.
        """
        return (
            "Prints hello world."
        )

    @classmethod
    def main(cls, options: Namespace) -> None:
        """
        Entrypoint for HelloWorld
        """
        logger = Logger.get_logger(cls.__tool_name__())
        logger.info(cls.__get_description__())

        output_string = f"Hello World, from {options.from_flag}"

        logger.info(f"From flag = {options.from_flag}.")
        logger.info(f"Output string = {output_string}")
        record_json = {"message": output_string}

        with open(options.output, 'w', encoding='utf-8') as o:
            json.dump(record_json, o, ensure_ascii=False, indent=4)
        logger.info(f"JSON response saved in {options.output}")

        return output_string
