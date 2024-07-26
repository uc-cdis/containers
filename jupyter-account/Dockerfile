# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

# Use ubuntu for our image
FROM ubuntu:22.04

# User
USER root

# Updating Ubuntu packages
RUN apt-get update && yes|apt-get upgrade
RUN DEBIAN_FRONTEND="noninteractive" apt-get install -yq pkg-config g++ bzip2 gcc libncurses-dev make zlib1g-dev libbz2-dev liblzma-dev openjdk-8-jre-headless

# Adding curl
RUN apt-get install -y curl

# Anaconda installing
RUN curl -O https://repo.anaconda.com/archive/Anaconda3-2020.02-Linux-x86_64.sh
RUN bash Anaconda3-2020.02-Linux-x86_64.sh -b
RUN rm Anaconda3-2020.02-Linux-x86_64.sh

# Set path to conda
ENV PATH /root/anaconda3/bin:$PATH

# Updating Anaconda packages
RUN conda update conda
RUN conda update anaconda
RUN conda update --all

# Install vcftools
RUN curl -OL https://github.com/vcftools/vcftools/releases/download/v0.1.16/vcftools-0.1.16.tar.gz
RUN tar xvfz vcftools-0.1.16.tar.gz \
    && rm vcftools-0.1.16.tar.gz
RUN cd vcftools-0.1.16 \
    && ./configure \
    && make \
    && make install \
