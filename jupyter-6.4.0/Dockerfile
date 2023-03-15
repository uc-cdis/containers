# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM quay.io/cdis/scipy-notebook:notebook-6.4.0
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
ENV R_BASE_VERSION 4.1.0

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
        libssl1.1 \
        libssl-dev \
        libbz2-dev \
        libcurl4-gnutls-dev \
        liblzma-dev \
        locales \
        openjdk-8-jdk \
        make \
        automake \
        perl \
        pkg-config \
        tzdata \
        vim \
        zlib1g \
        zlib1g-dev

## Now install R and littler, and create a link for littler in /usr/local/bin
#RUN apt-get update \
#	&& apt-get install -t unstable -y --no-install-recommends \
#		littler \
#    r-cran-littler \
#		r-base=${R_BASE_VERSION}-* \
#		r-base-dev=${R_BASE_VERSION}-* \
#		r-recommended=${R_BASE_VERSION}-* \
#	&& ln -s /usr/lib/R/site-library/littler/examples/install.r /usr/local/bin/install.r \
#	&& ln -s /usr/lib/R/site-library/littler/examples/install2.r /usr/local/bin/install2.r \
#	&& ln -s /usr/lib/R/site-library/littler/examples/installGithub.r /usr/local/bin/installGithub.r \
#	&& ln -s /usr/lib/R/site-library/littler/examples/testInstalled.r /usr/local/bin/testInstalled.r \
#	&& install.r docopt \
#	&& rm -rf /tmp/downloaded_packages/ /tmp/*.rds \

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

#
# R packages including IRKernel which gets installed globally.
# See https://github.com/rocker-org/rocker/blob/master/r-base/Dockerfile
#
RUN conda config --set unsatisfiable_hints True && \
    conda config --system --append channels r && \
    conda install --quiet --yes \
    'rpy2' \
    "r-base=$R_BASE_VERSION" \
    'r-irkernel' \
    'r-plyr' \
    'r-devtools' \
    'r-tidyverse' \
    'r-shiny' \
    'r-rmarkdown' \
    'r-forecast' \
    'r-rsqlite' \
    'r-reshape2' \
    'r-nycflights13' \
    'r-caret' \
    'r-rcurl' \
    'r-crayon' \
    'r-randomforest' \
    'r-rmysql' \
    'r-gplots' \
    'r-gtools' \
    'r-catools' \
    && conda clean -tipsy && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

RUN conda install -c bioconda nextflow

COPY --chown=jovyan:users resources/custom.js /home/$NB_USER/.jupyter/custom/
COPY --chown=jovyan:users resources/jupyter_notebook_config.py /home/$NB_USER/.jupyter/tmp.py
RUN cat /home/$NB_USER/.jupyter/tmp.py >> /home/$NB_USER/.jupyter/jupyter_notebook_config.py && rm /home/$NB_USER/.jupyter/tmp.py

# This fails ...
#RUN conda install -c r r-stringi

RUN echo "load.lib<-c('httr','jsonlite','dplyr','gplots','ggplot2','ggpubr','RColorBrewer','xml2','repr','VennDiagram'); install.lib<-load.lib[!load.lib %in% installed.packages()]; install.packages(install.lib,dependencies=TRUE, repos='http://cran.us.r-project.org', type='source')" | R --no-save
RUN echo 'if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager",dependencies=TRUE, repos="http://cran.us.r-project.org"); BiocManager::install(ask=FALSE)' | R --no-save
RUN echo "load.s3<-c('maftools', 'phyloseq', 'DESeq2', 'dada2', 'vcfR'); install.s3<-load.s3[!load.s3 %in% installed.packages()]; for(s3 in install.s3) BiocManager::install(s3, ask=FALSE);" | R --no-save
