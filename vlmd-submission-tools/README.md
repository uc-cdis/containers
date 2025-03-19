# vlmd-submission-tools

Python CLI with subcommands to support argo workflows for VLMD submission.

## Installation

1. Install poetry if you don't already have it (https://python-poetry.org/)
2. Install package `poetry install` (Note: poetry can manage environments but you can also generate a virtual environment yourself; regardless always build in a venv).

## Submission workflow

The following subcommands are executed for the VLMD dictionary submission and validation:

```
vlmd-submission-tools GetDictionaryUrl -d <indexd guid> -o <local json output>
vlmd-submission-tools ReadAndValidateDictionary -f <dictionary file name> -j <path to json dictionary> -t <dictionary title> -u <dictionary url> -o <local json output>
vlmd-submission-tools UploadDictionaryToMds -j <path to json dictionary> -n <dictionary name> -s <mds studyid> -o <local json output>
```

Each task requires a `-o` parameter to specify the local JSON output parameter artifact file
used in workflows, eg

`-o /tmp/url_parameters.json`

### Fence client credentials

#### Create the client

Some of the subcommands utilize fence client-credentials.

The credentials can be generated with the
[`fence-create`](https://github.com/uc-cdis/fence#fence-create-automating-common-tasks-with-a-command-line-interface)
command. You may have to delete any old clients if they exist.

```
kubectl exec -it $(gen3 pod fence-deployment) -c fence -- /bin/bash -c "fence-create client-delete --client vlmd_client
kubectl exec -it $(gen3 pod fence-deployment) -c fence -- /bin/bash -c "fence-create client-create --client vlmd_client --grant-types client_credentials --expires-in <DAYS>
```

Save the credentials. These can then be written to a json file and deployed as a kubernetes secret.

You may have to re-sync your `user.yaml` file after creating a new client.

#### Credentials secrets

For a production environment your credentials secret can be
deployed via
[`g3auto`](https://github.com/uc-cdis/cloud-automation/blob/9042162/doc/secrets.md)
or rotatated periodically via a `cloud-automation` job.

Create a new file for the credentials, for example
`Gen3Secrets/g3auto/vlmd-fence-client/fence_client_credentials.json`.
Edit the file to contain the credentials, using keys
from the config file:

```
{
    <config.CLIENT_ID_CONFIG>: <client_id>,
    <config.CLIENT_SECRET_CONFIG>: <client_secret>
}
```

Create the kubernetes secret

```
gen3 secrets sync
```

The name and keys for the kubernetes secret are specified in
environment variables that are read by the `common/config.py` module.

#### Fence client permissions

The fence client will need some permissions set in the `user.yaml` file.
For example, use the following if your fence client name is `vlmd_client` and
the `authz` of the indexd upload is `/programs/DEV`:

```
  vlmd_client:
    policies:
    - mds_admin
    - indexd_admin
    - audit_reader
    - requestor_admin
    - programs.DEV-admin
```

Include the following line in the `fence-config.yaml`:

```
CLIENT_CREDENTIALS_ON_DOWNLOAD_ENABLED: True
```

The fence version in your commons should be `9.2.0` or higher.

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

## Running locally

To see the available subcommands:

```
vlmd-submission-tools
```

To access the help documentation for a particular subcommand:

```
vlmd-submission-tools <subcommand> -h
```

The Gen3 commons hostname (eg, `qa-heal.planx-pla.net`) should be set as the environment variable `GEN3_HOSTNAME`.

The fence client-credentials are read from JSON in a local kubernetes secret.
You could run a kubernetes cluster locally, say via Docker Desktop, for storing the kubernetes secret.
The secret should mimic the structure of the `g3auto` secret in your commons, ie,
there is a main key that is derived from the name of the file
that stores the secrets.

For example, with Docker Desktop running, create your local kubernetes secret

```
kubectl create secret generic <CLIENT_SECRET_NAME> --from-file=fence_client_credentials.json=fence_client_credentials.json
```

where the local file `fence_client_credentials.json` has the following structure:

```
{
    <config.CLIENT_ID_CONFIG>: <client_id>,
    <config.CLIENT_SECRET_CONFIG>: <client_secret>
}
```

You will also need to set environment variables for the secret name, for example

```
export CLIENT_SECRET_NAME=vlmd-fence-client-g3auto
export CLIENT_SECRET_KEY_CONFIG=fence_client_credentials.json
export CLIENT_SECRET_NAMESPACE=default
```

The namespace will be `default` for your local environment and will likely be `argo` for a qa/production environment.
