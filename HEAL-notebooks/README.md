# HEAL Notebook Containers

---
## About

Notebooks for use in HEAL workspaces live here. Each directory
corresponds to an image that can be referenced as a notebook in
a HEAL workspace.

Notebooks stored here are hosted on quay in the [cdis/heal-notebooks](https://quay.io/repository/cdis/heal-notebooks)
repo.

Pushing to a directory within `HEAL-notebooks` automatically generates an image with these tags:

- `{directory}__latest`
- `{directory}__{branch}`
- `{directory}__{commit_sha}`

All contents within the directory will be copied into the home directory of the image as well.

If the directory contains a list of dependencies in `requirements.txt`, then those dependencies will be installed
automatically (and the `requirements.txt` file won't be included in the image).

We're currently switching to the 'combined_tutorials' directory for all HEAL tutorial notebooks. We're keeping the
individual notebook directories for now incase they may be needed in the near future. Please apply all tutorial notebook
updates to the 'combined_tutorials' directory.

## Adding a Notebook

Create a new directory within `HEAL-notebooks`

Add any files and/or nested directories needed to run the notebook.

Push all changes within the new directory to github

Ex:

Pushing a simple notebook with some dependencies and some data
```
$ mkdir HEAL-notebooks/plain_example
$ cp plain_notebook.ipynb HEAL-notebooks/plain_example/
$ echo "numpy" > HEAL-notebooks/plain_example/requirements.txt
$ mkdir HEAL-notebooks/plain_example/data
$ echo "data,moredata" > HEAL-notebooks/plain_example/data/my.csv
```
The directory in the containers repo is now:
```
.
├── HEAL-notebooks
│   ├── Dockerfile
│   ├── plain_example
│   │   ├── data
│   │   │   └── my.csv
│   │   ├── plain_notebook.ipynb
│   │   └── requirements.txt
│   └── README.md
```
So running
```
$ git add HEAL-notebooks/plain_example
$ git commit -m "add plain example notebook"
$ git push
```

Will trigger an automatic build of an image accessible by any of these tags:
`plain_exaple__latest`,`plain_exaple__{branch}`,`plain_exaple__{commit_sha}`
in the `uc-cdis/heal-notebooks` repo on quay. The home directory in that image
will look like this:
```
.
├── data
│   └── my.csv
├── plain_notebook.ipynb
```

## Caveats

- Since we can't push multiple images at a time via github actions, only one notebook can be built at a time.
  If a user pushes their branch with changes in multiple subdirectories of `HEAL-notebooks/`,
  then the `push-image` workflow will exit without updating images.

- This workflow should support building most, but not all notebook images. Notebooks with non-standard
  dependencies will require their own Dockerfiles and should not be stored in this directory.

- There must be at least 2 commits on the working branch in order to trigger a build (so that the
  workflow can detect changes).
