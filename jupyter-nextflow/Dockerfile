# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM jupyter/scipy-notebook:2023-03-13
USER root

#
# R pre-requisites
#  https://github.com/rocker-org/rocker/blob/master/r-base/Dockerfile
#
## Configure default locale, see https://github.com/rocker-org/rocker/issues/19
RUN echo "en_US.UTF-8 UTF-8" >> /etc/locale.gen \
	&& locale-gen en_US.utf8 \
	&& /usr/sbin/update-locale LANG=en_US.UTF-8

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV R_BASE_VERSION 3.6.3

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        autoconf \
        ca-certificates \
        fonts-dejavu \
        fonts-texgyre \
        gfortran \
        gcc \
        jq \
        less \
        libssl3 \
        libssl-dev \
        libbz2-dev \
        libcurl4-gnutls-dev \
        liblzma-dev \
        locales \
        openjdk-11-jdk \
        make \
        automake \
        perl \
        pkg-config \
        tzdata \
        vim \
        zlib1g \
        zlib1g-dev

RUN apt-get clean \
 	&& rm -rf /var/lib/apt/lists/*

#
# !!!!!NOTE!!!!!
# Do not install conda, python, pip, etc dependencies as root
# It screws up directory permissions
#
USER $NB_UID
WORKDIR /home/$NB_USER

RUN pip install --upgrade nbconvert

COPY --chown=jovyan:users resources/custom.js /home/$NB_USER/.jupyter/custom/
COPY --chown=jovyan:users resources/jupyter_notebook_config.py /home/$NB_USER/.jupyter/tmp.py
RUN cat /home/$NB_USER/.jupyter/tmp.py >> /home/$NB_USER/.jupyter/jupyter_notebook_config.py && rm /home/$NB_USER/.jupyter/tmp.py

RUN conda install -c bioconda nextflow
