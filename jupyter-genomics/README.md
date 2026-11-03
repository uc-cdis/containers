# jupyter-genomics

A **slim** Jupyter workspace image for testing software-library requirements.

It is derived from `jupyter-rcc` but stripped down: no preinstalled domain
packages, no reference genomes. The goal is a small base where users install
their own R and Python packages at runtime (and have those installs persist),
so the actual dependency footprint of a workflow can be tested from a clean
starting point.

## What's included

- **JupyterLab** + a **Python kernel** (`ipykernel`) and the classic notebook
  frontend.
- **R** (`r-base`) + **IRkernel**, registered so the R kernel is selectable in
  JupyterLab. No R packages are preinstalled.
- General-purpose **compilers and system dev libraries** (gcc/g++/gfortran,
  BLAS/LAPACK, and the common `-dev` libraries) so that user-installed CRAN
  packages compile without hitting a missing-system-library wall.
- **Download / export disabled and locked** in the JupyterLab UI
  (docmanager download, filebrowser download, notebook export), consistent with
  the secure-workspace requirement that data should not leave the environment.

## What's NOT included (install at runtime)

- No `requirements.txt` / preinstalled Python science stack
  (numpy, scipy, pandas, etc.).
- No SigProfiler and **no reference genome download** (keeps the image small).
- No preinstalled R packages (tidyverse, devtools, pdftools, magick, etc.).

## Persistent user installs

Both R and Python user installs are pointed at the persistent drive
(`/home/jovyan/pd`), so packages a user installs survive workspace restarts
with no manual setup:

- **R:** `R_LIBS_USER=/home/jovyan/pd/r_libraries`
  ```r
  install.packages("somepkg")   # no lib= needed
  # restart the R kernel, then:
  library(somepkg)
  ```
- **Python:** `PYTHONUSERBASE=/home/jovyan/pd/py_libraries`
  ```bash
  pip install --user somepkg    # lands on the persistent drive
  # restart the kernel, then import
  ```

The `pd/r_libraries` and `pd/py_libraries` directories are created at startup
by `start-notebook.sh` (they cannot be created at build time because `pd` is a
runtime mount).

## Persistent tool config

`PD=/home/jovyan/pd` is set, and other user-level tool state also lives on it:

| What | Location |
| --- | --- |
| Jupyter kernels (`ipykernel install --user`, etc.) | `pd/jupyter/kernels` (`~/.local/share/jupyter/kernels` is a symlink to it) |
| `git config --global` | `pd/.config/git/config` (`GIT_CONFIG_GLOBAL`) |
| `gh` | `pd/.config/gh` (`GH_CONFIG_DIR`) |
| pre-commit | `pd/.cache/pre-commit` (`PRE_COMMIT_HOME`) |
| uv Pythons / tools / cache | `pd/.uv/{python,tools,cache}`, executables in `pd/.uv/bin` |
| Your own binaries | `pd/tools/bin` |

`uv` itself is installed in the image (`/usr/local/bin/uv`). The kernels the
image ships (Python, R, Stata) live in `/usr/local/share/jupyter/kernels`, so
they update with the image.

On `PATH`, `pd/.uv/bin`, `pd/tools/bin` and `pd/py_libraries/bin` come first,
ahead of software-library modules, so a tool on `pd` overrides one of the same
name from `/apps`.


## CI

Pushing changes under `jupyter-genomics/**` triggers
`.github/workflows/build_jupyter_genomics_image.yml`, which builds and pushes
`jupyter-notebook:genomics-<branch>` (linux/amd64).
