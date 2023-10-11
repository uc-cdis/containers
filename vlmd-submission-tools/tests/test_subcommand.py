"""Tests the `vlmd_submission_tools.subcommands.base.Subcommand` class"""
import pytest

from utils import captured_output
from vlmd_submission_tools.__main__ import main
from vlmd_submission_tools.subcommands import Subcommand


class TestSubcommand:
    class Example(Subcommand):
        @classmethod
        def __add_arguments__(cls, subparser):
            pass

        @classmethod
        def __main__(cls, options):
            pass

        @classmethod
        def __get_description__(cls):
            return "Example description"

    def test_get_name(self):
        assert TestSubcommand.Example.__tool_name__() == "Example"
        assert Subcommand.__tool_name__() == "Subcommand"

    def test_get_description(self):
        assert TestSubcommand.Example.__get_description__() == "Example description"
        assert not Subcommand.__get_description__()

    def test_no_inputs(self):
        # invalid subcommand
        with captured_output() as (_, stderr):
            with pytest.raises(SystemExit) as context:
                main(args=["Example"])
        assert "invalid choice: 'Example'" in stderr.getvalue()

    def test_extra_subparser(self):
        # invalid args
        with captured_output() as (_, stderr):
            with pytest.raises(SystemExit) as context:
                main(args=["Example", "--fake"], extra_subparser=TestSubcommand.Example)
        assert "unrecognized arguments: --fake" in stderr.getvalue()
