"""Tests for the ``vlmd_submission_tools.subcommands.HelloWorld`` subcommand"""
from typing import NamedTuple

import json

from utils import cleanup_files
from vlmd_submission_tools.subcommands import HelloWorld


class MockArgs(NamedTuple):
    from_flag: str
    output: str


class TestHelloWorldSubcommand:
    # Template for setting up test for subcommand modules
    def get_mock_args(self):
        return MockArgs(
            from_flag="VLMD",
            output="tmp.json",
        )

    def test_hello_world(self):
        args = self.get_mock_args()
        expected_message=f"Hello World, from {args.from_flag}"
        expected_json={"message": expected_message}

        try:
            result = HelloWorld.main(options=args)
            assert result == expected_message

            with open(args.output, 'r') as fh:
                result_json = json.load(fh)
            assert json.dumps(result_json) == json.dumps(expected_json)
        finally:
            cleanup_files([args.output])
