FROM quay.io/cdis/jupyterlab-generic:drb-jupyter-persistance

USER root

# Install system dependencies
RUN dnf update -y && dnf install -y \
    gcc-c++ \
    ghostscript-devel \
    gsl-devel \
    gzip \
    libcurl-devel \
    libssh2-devel \
    libxml2-devel \
    openssl \
    openssl-devel \
    python3.14 \
    python3.14-pip \
    python3.14-setuptools \
    python3.14-pip-wheel \
    python3.14-devel \
    tar \
    unzip \
    wget \
    zlib-devel \
    && dnf clean all

# Define the ve helper system-wide so the image doesn't create ~/.bashrc;
# that lets jupyterlab-start.sh link ~/.bashrc into pd
RUN echo 've() { mkdir -p virtualenv; cd virtualenv; VENV="$1"; python3.14 -m venv "$VENV" --system-site-packages; . "$VENV/bin/activate"; python3.14 -m ipykernel install --user --name="$VENV"; deactivate; }' \
    > /etc/profile.d/ve.sh

# Terminals are login shells and the base image's .bash_profile (in pd) may be empty,
# so load ~/.bashrc from here unless .bash_profile already does
RUN echo '[ -n "$BASH_VERSION" ] && shopt -q login_shell && ! grep -qs bashrc ~/.bash_profile && case $- in *i*) [ -f ~/.bashrc ] && . ~/.bashrc;; esac' \
    > /etc/profile.d/zz-load-bashrc.sh

# Let the file browser show hidden files (dotfiles like .bashrc, .config)
RUN mkdir -p /usr/local/etc/jupyter && \
    echo 'c.ContentsManager.allow_hidden = True' \
    > /usr/local/etc/jupyter/jupyter_server_config.py

USER jovyan

# Persist JupyterLab settings and layouts in pd
ENV JUPYTERLAB_SETTINGS_DIR=/home/jovyan/pd/.jupyter/lab/user-settings
ENV JUPYTERLAB_WORKSPACES_DIR=/home/jovyan/pd/.jupyter/lab/workspaces

# Install everything from requirements.txt
# (must come before PYTHONUSERBASE is set, or these would install into pd
# and be hidden when pd is mounted)
COPY requirements.txt .
RUN pip3.14 install --no-cache-dir -r requirements.txt

# Copy notebook directory
COPY combined_demos/ $HOME/

# Persist user-installed Python packages in pd, same as jupyter-genomics:
# `pip install --user <pkg>` goes to pd/py_libraries and CLI tools land on PATH
ENV PYTHONUSERBASE="/home/jovyan/pd/py_libraries"
ENV PATH="/home/jovyan/pd/py_libraries/bin:${PATH}"
# Keep JupyterLab finding the base image's install in ~/.local
ENV JUPYTERLAB_DIR="/home/jovyan/.local/share/jupyter/lab"
ENV JUPYTER_CONFIG_PATH="/home/jovyan/.local/etc/jupyter"

# Show hidden files in the file browser by default (users can still turn it off)
RUN mkdir -p /home/jovyan/.local/share/jupyter/lab/settings && \
    echo '{"@jupyterlab/filebrowser-extension:browser": {"showHiddenFiles": true}}' \
    > /home/jovyan/.local/share/jupyter/lab/settings/overrides.json
