# Use the specified base image
FROM anibali/pytorch:1.13.1-cuda11.7-ubuntu22.04

# Change the USER to `root` to have necessary privileges to perform apt-get commands
USER root
RUN apt-get update && apt-get -y upgrade

# Upgrade pillow to the latest stable version
RUN pip install --upgrade pillow

# install openssl 3.0.8 as it is required for FIPS compliance.
RUN mamba install -yc conda-forge openssl=3.0.8

# Change USER back to the one in the anibali image to limit privileges
USER user
