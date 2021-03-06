# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM quay.io/cdis/scipy-notebook:5cfa60996e84
USER root

## Configure default locale, see https://github.com/rocker-org/rocker/issues/19
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
	&& locale-gen en_US.utf8 \
	&& /usr/sbin/update-locale LANG=en_US.UTF-8

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    autoconf \
    bc \
    ca-certificates \
    fonts-dejavu \
    fonts-texgyre \
    gfortran \
    gcc \
    jq \
    make \
    automake \
    perl \
    less \
    libssl1.1 \
    libssl-dev \
    libbz2-dev \
    locales \
    pkg-config \
    tzdata \
    vim \
    zlib1g \
    zlib1g-dev \
    libcurl4-gnutls-dev \
    liblzma-dev \
    openjdk-8-jdk

RUN apt-get clean \
 	&& rm -rf /var/lib/apt/lists/*

#
# !!!!!NOTE!!!!!
# Do not install conda, python, pip, etc dependencies as root
# It screws up directory permissions
#
USER $NB_UID
WORKDIR /home/$NB_USER


RUN pip install --upgrade nbconvert==5.6.1 && \
   pip install --upgrade gen3


#
# R packages including IRKernel which gets installed globally.
# See https://github.com/rocker-org/rocker/blob/master/r-base/Dockerfile
#
RUN conda config --set unsatisfiable_hints True && \
    conda clean -tipsy && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

RUN wget https://github.com/arq5x/lumpy-sv/releases/download/0.3.0/lumpy-sv.tar.gz; \
    tar -zxvf lumpy-sv.tar.gz lumpy-sv; rm lumpy-sv.tar.gz; \
    cd lumpy-sv; make; cp bin/* /usr/local/bin/.; \
    rm -rf data/ src/ .git;

COPY --chown=jovyan:users resources/custom.js /home/$NB_USER/.jupyter/custom/
COPY --chown=jovyan:users resources/jupyter_notebook_config.py /home/$NB_USER/.jupyter/tmp.py
RUN cat /home/$NB_USER/.jupyter/tmp.py >> /home/$NB_USER/.jupyter/jupyter_notebook_config.py && rm /home/$NB_USER/.jupyter/tmp.py

RUN jupyter labextension install jupyterlab-plotly
