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

## Build / test locally

```bash
docker build -t jupyter-genomics:test .

# start it, mounting a fake persistent drive
mkdir -p /tmp/fakepd
docker run --rm -p 8899:8888 -v /tmp/fakepd:/home/jovyan/pd \
    jupyter-genomics:test --ip=0.0.0.0 --IdentityProvider.token=''
# open http://localhost:8899/lab
```

Verify persistence paths resolve:

```bash
docker run --rm -v /tmp/fakepd:/home/jovyan/pd jupyter-genomics:test \
    bash -c 'echo "R:"; R -e ".libPaths()" -q; echo "PY:"; python3 -c "import site; print(site.getusersitepackages())"'
```

## CI

Pushing changes under `jupyter-genomics/**` triggers
`.github/workflows/build_jupyter_genomics_image.yml`, which builds and pushes
`jupyter-notebook:genomics-<branch>` (linux/amd64).
