FROM rocker/r-ver:4.1.0 as r-base
FROM python:3.9-slim

COPY --from=r-base / /

COPY ./install_packages.R /opt
COPY ./requirements.txt /opt

RUN apt-get update && apt-get install -y \
       libxml2-dev \
	&& apt-get clean && apt-get autoremove \
	&& rm -rf /var/lib/apt/lists/*

ENV LD_LIBRARY_PATH=/usr/local/lib

RUN pip install -r /opt/requirements.txt
RUN Rscript /opt/install_packages.R

ENTRYPOINT [ "/bin/bash" ]
