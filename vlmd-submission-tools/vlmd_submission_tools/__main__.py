"""
Main entrypoint for all vlmd-submission-tools.
"""
import argparse
import datetime
import sys
from signal import SIG_DFL, SIGPIPE, signal

from vlmd_submission_tools.common.logger import Logger
from vlmd_submission_tools.subcommands import (
    HelloWorld,
    GetDictionaryUrl,
    ReadAndValidateDictionary,
    UploadDictionaryToMds
)

signal(SIGPIPE, SIG_DFL)


def main(args=None, extra_subparser=None) -> None:
    """
    The main method for vlmd-submission-tools.
    """
    # Setup logger
    Logger.setup_root_logger()

    logger = Logger.get_logger("main")

    # Print header
    logger.info("-" * 75)
    logger.info("Program Args: vlmd-submission-tools " + " ".join(sys.argv[1::]))
    logger.info("Date/time: {0}".format(datetime.datetime.now()))
    logger.info("-" * 75)
    logger.info("-" * 75)

    # Get args
    p = argparse.ArgumentParser("VLMD Submission Tools")
    subparsers = p.add_subparsers(dest="subcommand")
    subparsers.required = True

    # Subcommands
    HelloWorld.add(subparsers=subparsers)
    GetDictionaryUrl.add(subparsers=subparsers)
    ReadAndValidateDictionary.add(subparsers=subparsers)
    UploadDictionaryToMds.add(subparsers=subparsers)

    if extra_subparser:
        extra_subparser.add(subparsers=subparsers)

    options = p.parse_args(args)

    # Run
    cls = options.func(options)

    # Finish
    logger.info("Finished!")


if __name__ == "__main__":
    main()
