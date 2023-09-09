# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM quay.io/cdis/amazonlinux:latest
USER root

RUN  dnf install -y glibc-locale-source && localedef -i en_US -f UTF-8 en_US.UTF-8

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8

ENV R_BASE_VERSION=3.6.3


RUN dnf upgrade && \
    dnf install -y \
    autoconf \
    ca-certificates \
    dejavu-fonts-all \
    texlive-tex-gyre \
    gfortran \
    gcc \
    jq \
    less \
    openssl \
    openssl-devel \
    bzip2-devel \
    libcurl-devel \
    gnutls-devel \
    xz-devel \
    glibc-locale-source \
    java-11-amazon-corretto \
    make \
    automake \
    perl \
    pkg-config \
    tzdata \
    vim \
    zlib \
    zlib-devel


RUN dnf clean all
ENV NB_UID jovyan
ENV NB_USER jovyan

RUN adduser -r -g users $NB_UID
USER $NB_UID
WORKDIR /home/$NB_USER

RUN python3 -m venv .venv \
    && source .venv/bin/activate \
    && python3 -m pip install --upgrade pip \
    && pip install --upgrade nbconvert


COPY --chown=jovyan:users resources/custom.js /home/$NB_USER/.jupyter/custom/
COPY --chown=jovyan:users resources/jupyter_notebook_config.py /home/$NB_USER/.jupyter/tmp.py
RUN ls -l
