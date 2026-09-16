FROM public.ecr.aws/amazonlinux/amazonlinux:2023-minimal

ARG NB_USER="jovyan"
ARG NB_UID="1010"
ENV NB_USER="${NB_USER}" \
    NB_UID="${NB_UID}" \
    HOME="/home/${NB_USER}"

USER root

RUN ln -s /usr/bin/python3.14 /usr/local/bin/python3 && \
    ln -s /usr/bin/python3.14 /usr/local/bin/python

RUN dnf upgrade --refresh && \
    dnf install -y \
    ca-certificates \
    gcc-c++ \
    ghostscript-devel \
    git \
    gsl-devel \
    gzip \
    libcurl-devel \
    libssh2-devel \
    libxml2-devel \
    openssl \
    openssl-devel \
    python3.14 \
    python3.14-pip \
    python3.14-pip-wheel \
    python3.14-setuptools \
    shadow-utils \
    tar \
    unzip \
    wget \
    which \
    zlib-devel && \
    dnf clean all


RUN useradd -u ${NB_UID} -m ${NB_USER}

USER jovyan
WORKDIR ${HOME}
ENV SHELL=/bin/bash
ENV PATH="${HOME}/.local/bin:${PATH}"

# Install everything from requirements.txt
COPY requirements.txt .
RUN pip3.14 install --no-cache-dir -r requirements.txt
RUN rm ${HOME}/requirements.txt

RUN python3.14 -m pip install --user \
    jupyterlab \
    ipykernel

RUN python -m ipykernel install --user --name=python3.14 --display-name "Python 3.14"

# Copy notebook directory
COPY combined_demos $HOME/combined_demos

USER root
COPY run.sh /run.sh
RUN chmod +x /run.sh
COPY start-notebook.sh /usr/local/bin/start-notebook.sh
RUN chmod +x /usr/local/bin/start-notebook.sh
USER jovyan

# Add virtual environment function to bashrc
RUN echo 'function ve(){ mkdir -p virtualenv; cd virtualenv; VENV="$1"; python3.14 -m venv $VENV --system-site-packages; source $VENV/bin/activate; python3.14 -m ipykernel install --user --name=$VENV; deactivate; }' >> /home/jovyan/.bashrc

CMD ["/run.sh"]
