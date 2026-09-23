# Generic Gen3 JupyterLab workspace

FROM public.ecr.aws/amazonlinux/amazonlinux:2023-minimal
LABEL maintainer="Center for Translational Data Science (CTDS)"
LABEL name="jupyterlab-generic"

# Configure environment for NB_USER since we are using generic amazonlinux base image,
# similar to https://github.com/uc-cdis/jupyter-superslim/Dockerfile
ARG NB_USER="jovyan"
ARG NB_UID="1010"
ARG NB_GID="1010"
ENV NB_USER="${NB_USER}" \
    NB_UID="${NB_UID}" \
    NB_GID="${NB_GID}" \
    HOME="/home/${NB_USER}"

# TODO: git, nodejs, and build are all required only to build jupyterlmod;
#       these can be dropped once jupyterlmod fix is available in PyPI.
# ncurses-compat-libs provides libncurses.so.5/libtinfo.so.5, required to load
# Stata's shared library (used by the nbstata kernel).
RUN dnf upgrade --refresh && \
    dnf install -y python3.14 python3.14-pip git \
        shadow-utils which ca-certificates ncurses-compat-libs && \
    curl -fsSL https://rpm.nodesource.com/setup_20.x | bash - && \
    dnf install -y nodejs && \
    dnf clean all

RUN ln -s /usr/bin/python3.14 /usr/local/bin/python3 && \
ln -s /usr/bin/python3.14 /usr/local/bin/python

# Create non-root user NB_USER
RUN groupadd -g ${NB_GID} ${NB_USER} && \
    useradd -u ${NB_UID} -g ${NB_USER} -M ${NB_USER} && \
    mkdir -p ${HOME} && \
    chown ${NB_USER}:${NB_USER} ${HOME} && \
    chmod 700 ${HOME} && \
    usermod -d ${HOME} ${NB_USER} && \
    usermod --shell /bin/bash ${NB_USER}

COPY jupyterlab-start.sh .
RUN chmod +x jupyterlab-start.sh && \
    chown ${NB_USER}:${NB_USER} /jupyterlab-start.sh

USER ${NB_USER}
WORKDIR ${HOME}

# Install Python/Jupyter packages as NB_USER
RUN python3.14 -m pip install --user --upgrade pip setuptools wheel && \
python3.14 -m pip install --user \
    jupyterlab \
    build && \
python3.14 -m pip install --user \
    jupyterlmod \
    git+https://github.com/pschumm/jupyter-lmod@pschumm/fix_hidden && \
python3.14 -m pip install --user jupyterlab-git \
    jupyter-archive \
    lckr-jupyterlab-variableinspector \
    jupyterlab-search-replace \
    ipykernel==6.31.0 && \
python3.14 -m ipykernel install --user \
    --name "Python-3.14.0" \
    --display-name "Python 3.14 (ipykernel)"

# Install nbstata (Stata kernel). Stata itself is not in the image; it is provided
# at runtime via lmod, and nbstata locates it on PATH once the module is loaded.
# The installer writes a config with an empty stata_dir when Stata is not found,
# so remove it (and ~/.config if left empty) to keep PATH discovery and the
# ~/.config persistence symlink in jupyterlab-start.sh working.
RUN python3.14 -m pip install --user nbstata && \
    python3.14 -m nbstata.install --user && \
    rm -rf ${HOME}/.config/nbstata && \
    rmdir --ignore-fail-on-non-empty ${HOME}/.config

EXPOSE 8888

# Enable lmod
ENV LMOD_CMD=/apps/lmod/lmod/libexec/lmod
ENV MODULEPATH=/apps/lmod/lmod/modulefiles
ENV LMOD_MODULERC=/apps/lmod/lmod/.modulerc.lua

# Make sure bash is the default shell within JupyterLab terminal
ENV SHELL=/bin/bash

# Add user binary paths to environment PATH so CLI commands execute globally
ENV PATH="${HOME}/.local/bin:${PATH}"
# Add the user path to PYTHONPATH for user installed modules
ENV PYTHONPATH="${HOME}/.local/lib/python3.14/site-packages"

CMD ["/jupyterlab-start.sh"]
