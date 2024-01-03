# Use the specified base image
FROM nvcr.io/nvidia/cuda:11.8.0-base-ubuntu22.04

RUN apt-get purge -y --auto-remove openssl && apt-get autoremove && apt-get autoclean

RUN apt-get update && apt-get -y upgrade && apt install -y wget

RUN apt install -y build-essential && \
    apt-get install -y python3 && \
    apt-get install -y python3-pip

# install openssl 3.0.8 as it is required for FIPS compliance.
WORKDIR /tmp
RUN wget https://www.openssl.org/source/openssl-3.0.8.tar.gz && \
    tar -xzvf openssl-3.0.8.tar.gz && \
    rm openssl-3.0.8.tar.gz

WORKDIR /tmp/openssl-3.0.8
RUN ./Configure enable-fips && \
    make && \
    make install

# Changing adding `/usr/local/lib` as a prefix to LD_LIBRARY_PATH will
# give precedence to OpenSSL 3.0.8 library files over the 3.0.2
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH

# Clean up the temporary directory
WORKDIR /
RUN rm -rf /tmp/openssl-3.0.8
