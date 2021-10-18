# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.
FROM quay.io/cdis/jupyter-6.4.0:latest
USER root

COPY ./requirements.txt /opt

RUN apt-get update && apt-get install -y \
       libxml2-dev \
    && apt-get clean && apt-get autoremove \
    && rm -rf /var/lib/apt/lists/*

ENV LD_LIBRARY_PATH=/usr/local/lib
RUN pip install -r /opt/requirements.txt \
    pip install --upgrade gen3

RUN echo "load.lib<-c('tinytex','rmarkdown','tidyverse','devtools'); install.lib<-load.lib[!load.lib %in% installed.packages()]; install.packages(install.lib,dependencies=TRUE, repos='http://cran.us.r-project.org', type='source')" | R --no-save
