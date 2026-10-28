FROM quay.io/cdis/jupyterlab-generic:master

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

RUN echo '[ -n "$BASH_VERSION" ] && case $- in *i*) [ -f ~/.bashrc ] && . ~/.bashrc;; esac' \
    > /etc/profile.d/zz-load-bashrc.sh

USER jovyan

ENV JUPYTERLAB_SETTINGS_DIR=/home/jovyan/pd/.jupyter/lab/user-settings
ENV JUPYTERLAB_WORKSPACES_DIR=/home/jovyan/pd/.jupyter/lab/workspaces
ENV PYTHONPATH="/home/jovyan/pd/py_libraries:${PYTHONPATH}"

# Install everything from requirements.txt
COPY requirements.txt .
RUN pip3.14 install --no-cache-dir -r requirements.txt

# Copy notebook directory
COPY combined_demos/ $HOME/

# Add virtual environment function to bashrc
RUN echo 'function ve(){ mkdir -p virtualenv; cd virtualenv; VENV="$1"; python3.14 -m venv $VENV --system-site-packages; source $VENV/bin/activate; python3.14 -m ipykernel install --user --name=$VENV; deactivate; }' >> /home/jovyan/.bashrc && \
    echo '[ -f ~/pd/.bashrc ] && . ~/pd/.bashrc' >> /home/jovyan/.bashrc
