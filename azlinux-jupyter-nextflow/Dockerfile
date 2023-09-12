############################ Jupyter-nextflow With AzLinux ###################
ARG ROOT_CONTAINER=quay.io/cdis/azlinux-jupyter-scipy:scipy-chore_change_nf_base_img

ARG BASE_CONTAINER=$ROOT_CONTAINER
FROM $BASE_CONTAINER
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

USER $NB_UID
WORKDIR /home/$NB_USER


RUN pip install --upgrade nbconvert

COPY --chown=jovyan:users resources/custom.js /home/$NB_USER/.jupyter/custom/
COPY --chown=jovyan:users resources/jupyter_notebook_config.py /home/$NB_USER/.jupyter/tmp.py

RUN cat /home/$NB_USER/.jupyter/tmp.py >> /home/$NB_USER/.jupyter/jupyter_server_config.py && rm /home/$NB_USER/.jupyter/tmp.py

#TODO: need to install bounty castle

RUN mamba install -yc bioconda nextflow==22.10.6
