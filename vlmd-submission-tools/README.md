# vlmd-submission-tools

Python CLI with various subcommands to support the argo HEAL workflows.

## Installation

1. Install poetry if you don't already have it (https://python-poetry.org/)
2. Install package `poetry install` (Note: poetry can manage environments but you can also generate a virtual environment yourself; regardless always build in a venv).

## Basic usage

To see the available subcommands:

```
vlmd-submission-tools
```

To access the help documentation for a particular subcommand:

```
vlmd-submission-tools <subcommand> -h
```

The Gen3 commons hostname (eg, `qa-heal.planx-pla.net`) should be set as the environment variable `GEN3_HOSTNAME`.

### Submission workflow

The following subcommands are executed for the VLMD dictionary submission and validation:

```
vlmd-submission-tools GetDictionaryUrl -d <indexd guid>
vlmd-submission-tools ReadAndValidateDictionary -f <dictionary file name> -l <local file path> -u <dictionary url>
vlmd-submission-tools UploadDictionaryToMds -j <path to json dictionary> -n <dictionary name> -s <mds studyid>
```

### Fence client credentials

Some of the subcommands utilize fence client credentials. The
credentials are currently read from a kubernetes secret. The secret name and keys are configured in `common/config.py`.

The fence client will need some permissions set in the user.yaml file.
For example, use the following if your fence client name is `vlmd_client` and the `authz` of the indexd upload is `/programs/DEV`:

```
  vlmd_client:
    policies:
    - mds_admin
    - indexd_admin
    - audit_reader
    - requestor_admin
    - programs.DEV-admin
```

## Adding a new subcommand

1. Create a python file in `vlmd_submission_tools/subcommands/`
2. Inherit from the `vlmd_submission_tools.subcommands.Subcommand` abstract base class.
3. Follow the subcommand API to implement your subcommand:

```python
 class MySubcommand(Subcommand): # This class name will be the subcommand to call on the command line
     @classmethod
     def __add_arguments__(cls, parser: ArgumentParser) -> None: # Define your subcommand-specific arguments
         """Add the subcommand params"""
         parser.add_argument(
             "inputs",
             help="Input to process.",
         )

     @classmethod
     def main(cls, options: Namespace) -> None: # All the main logic of your subcommand goes here
         """
         Entrypoint for MySubcommand
         """
         logger = Logger.get_logger(cls.__tool_name__()) # create a logger by importing this class: from vlmd_submission_tools.common.logger import Logger
         logger.info(cls.__get_description__())

         # do stuff...

     @classmethod
     def __get_description__(cls) -> str: # Define the subcommand description which will appear in CLI
         """
         Description of tool.
         """
         return (
             "This subcommand does really cool stuff. "
             "It outputs some things and handles some inputs."
         )
```
4. Import your subcommand class in `vlmd_submission_tools/subcommands/__init__.py`
5. Import your subcommand in `vlmd_submission_tools/__main__.py`
6. Add your subcommand class to the `vlmd_submission_tools.__main__.main` function where the other ones are called: `MySubcommand.add(subparsers=subparsers)`
7. Create unit tests.

If you need to add dependencies you must use the `poetry add ...` functionality.
