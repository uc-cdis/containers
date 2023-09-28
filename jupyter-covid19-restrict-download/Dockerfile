ARG ROOT_CONTAINER=quay.io/cdis/ubuntu:focal

FROM $ROOT_CONTAINER

LABEL maintainer="Jupyter Project <jupyter@googlegroups.com>"

# Fix DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# ---- Miniforge installer ----
# Default values can be overridden at build time
# (ARGS are in lower case to distinguish them from ENV)
# Check https://github.com/conda-forge/miniforge/releases
# Conda version
ARG conda_version="4.14.0"
# Miniforge installer patch version
ARG miniforge_patch_number="2"
# Package Manager and Python implementation to use (https://github.com/conda-forge/miniforge)
# - conda only: either Miniforge3 to use Python or Miniforge-pypy3 to use PyPy
# - conda + mamba: either Mambaforge to use Python or Mambaforge-pypy3 to use PyPy
ARG miniforge_python="Mambaforge"
# Miniforge archive to install
ARG miniforge_version="${conda_version}-${miniforge_patch_number}"

# Install all OS dependencies for notebook server that starts but lacks all
# features (e.g., download as all possible file formats)
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update --yes && \
    apt-get install --yes --no-install-recommends \
    python3.9 \
    python3-pip \
    tini \
    wget \
    git \
    curl \
    ca-certificates \
    sudo \
    locales \
    fonts-liberation \
    vim \
    run-one && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    echo "en_US.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen

RUN pip3 install JPype1 jupyter pandas numpy seaborn scipy matplotlib pyNetLogo SALib

RUN jupyter notebook --generate-config

RUN useradd -ms /bin/bash jupyter


RUN jupyter labextension disable @jupyterlab/docmanager-extension:download \
    && jupyter labextension disable @jupyterlab/filebrowser-extension:download


RUN pip uninstall nbconvert --yes

USER jupyter
WORKDIR /home/jupyter
EXPOSE 8888

ARG COVID_TOOLS_BRANCH=master
ADD --chown=jupyter:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/welcome.html /home/jupyter/
RUN touch /home/jupyter/welcome.html

ENTRYPOINT ["jupyter", "lab","--allow-root","--ip=0.0.0.0","--port=8888","--no-browser"]
