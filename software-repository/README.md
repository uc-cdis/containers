# Introduction

This folder contains tools for managing the software repository containing
analytic software for use from within Gen3 workspaces.

# Usage

After building and running the image, use

    docker exec -it gen3-workspace-admin bash --init-file /spack/share/spack/setup-env.sh

to get a shell from which you can use Spack to manage the software repository.

## Installing lmod

The latest version of `lmod` can be installed with

    spack install lmod@8.7.55

To make it easier to use:

    mkdir -p /apps/lmod/lmod/init
    cd /apps/lmod/lmod/init
    ln -s ../../../spack/linux-aarch64/lmod-8.7.55-fsamnguoh33bp5pt3vqn2h42v2mo5m4b/lmod/lmod/init/profile .
    mkdir -p /apps/lmod/lmod/libexec
    cd /apps/lmod/lmod/libexec
    ln -s ../../../spack/linux-aarch64/lmod-8.7.55-fsamnguoh33bp5pt3vqn2h42v2mo5m4b/lmod/lmod/libexec/lmod .

To control defaults, aliases, and hidden modules, we use a `.modulerc.lua` file
that needs to be copied into an appropriate location, e.g.:

    cp -p ~/lmod/.modulerc.lua /apps/lmod/lmod/.

To use `lmod`:

    source /apps/lmod/lmod/init/profile
    module use --append /apps/lmod/lmod/modulefiles

To regenerate module files (e.g., after installing new software):

    spack module tcl refresh --delete-tree

> [!NOTE]
> For some reason, I was not able to get projections working properly with
> `lmod/lua` modules, so for now I'm using `tcl` modules instead. This is
> presumably a fixable problem, and at some point we should probably switch over
> to `lmod/lua` modules for the best `lmod` experience.

## JupyterLab

### Dependencies for JupyterLab extensions

These are required for JupyterLab extensions. To keep things simple, we'll mark
them as implicit for now.

    spack install git
    spack mark --implicit git
    spack install ripgrep
    spack mark --implicit ripgrep

### IPython kernel

Install Python and mark as implicit (to avoid extra complexity):

    spack install python@3.14.0
    spack mark --implicit python@3.14.0

Create and activate virtual environment:

    spack load python@3.14.0
    python -m venv /apps/venv/python-3.14.0
    source /apps/venv/python-3.14.0/bin/activate

Install `ipykernel`:

    pip install --upgrade pip
    pip install ipykernel==6.31.0
    python -m ipykernel install --prefix=/apps --name "Python-3.14.0" --display-name "Python 3.14 (ipykernel)"

> [!NOTE]
> We might also consider using Spack environments here instead, though at the
> moment it seems like an additional complication without obvious added benefit.

## Python packages

Most of the data management and analytic capability when using an IPython kernel
is provided by Python packages. Below is a running list of those we provide in
our workspaces:

    spack install py-numpy@2.3.4 ^python@3.14.0
    spack install py-pandas@2.3.3 ^python@3.14.0
    spack install py-scipy@1.16.2 ^python@3.14.0
    spack install py-altair@5.5.0 ^python@3.14.0
