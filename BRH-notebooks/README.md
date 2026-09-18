# BRH Notebook Containers

---
## About

Notebooks for use in BRH workspaces live here. Each directory
corresponds to an image that can be referenced as a notebook in
a BRH workspace.

Notebooks stored here are hosted on quay in the [cdis/brh-notebooks](https://quay.io/repository/cdis/brh-notebooks)
repo.

Pushing to a directory within `BRH-notebooks` automatically generates an image with these tags:

- `{directory}__latest`
- `{directory}__{branch}`
- `{directory}__{commit_sha}`

All contents within the directory will be copied into the home directory of the image as well.

If the directory contains a list of dependencies in `pyproject.toml` and `poetry.lock`, then those dependencies will be installed
automatically (and the `pyproject.toml` and `poetry.lock` files won't be included in the image).

## Adding a Notebook

Create a new directory within `BRH-notebooks`

Add any files and/or nested directories needed to run the notebook.

Push all changes within the new directory to github

Ex:

Pushing a simple notebook with some dependencies and some data
```
$ mkdir BRH-notebooks/plain_example
$ cp plain_notebook.ipynb BRH-notebooks/plain_example/
$ echo "numpy" > BRH-notebooks/plain_example/requirements.txt
$ mkdir BRH-notebooks/plain_example/data
$ echo "data,moredata" > BRH-notebooks/plain_example/data/my.csv
```
The directory in the containers repo is now:
```
.
├── BRH-notebooks
│   ├── Dockerfile
│   ├── plain_example
│   │   ├── data
│   │   │   └── my.csv
│   │   ├── plain_notebook.ipynb
│   │   ├── pyproject.toml
│   │   └── poetry.lock
│   └── README.md
```
So running
```
$ git add BRH-notebooks/plain_example
$ git commit -m "add plain example notebook"
$ git push
```

Will trigger an automatic build of an image accessible by any of these tags:
`plain_exaple__latest`,`plain_exaple__{branch}`,`plain_exaple__{commit_sha}`
in the `uc-cdis/brh-notebooks` repo on quay. The home directory in that image
will look like this:
```
.
├── data
│   └── my.csv
├── plain_notebook.ipynb
```

## Caveats

- Since we can't push multiple images at a time via github actions, only one notebook can be built at a time.
  If a user pushes their branch with changes in multiple subdirectories of `BRH-notebooks/`,
  then the `push-image` workflow will exit without updating images.

- This workflow should support building most, but not all notebook images. Notebooks with non-standard
  dependencies will require their own Dockerfiles and should not be stored in this directory.

- There must be at least 2 commits on the working branch in order to trigger a build (so that the
  workflow can detect changes).
