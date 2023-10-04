## Background

This Dockerfile is created as an alternative to Jupyter's Scipy notebook ([link here](https://github.com/jupyter/docker-stacks/blob/main/images/scipy-notebook/Dockerfile)) while maintaining FIPS compliance. The scipy image is built on top of a hierarchy of docker images as depicted below.

![Block Diagram of jupyter scipy image](https://jupyter-docker-stacks.readthedocs.io/en/latest/_images/inherit.svg "Block Diagram of jupyter scipy image")

In order for this image to be FIPS compliant the base image that was supposed to be an `ubuntu LTS` is now replaced with AmazonLinux from CTDS ([link here](https://quay.io/repository/cdis/amazonlinux?tab=info))

Amazon linux container uses `yum` or `dnf` as it's package manager instead of `apt` on the former ubuntu based image, the sci-py docker file and all the other docker files on which this file is based, have been replaced with appropriate alternatives, with some mentions about packages whose alternatives were not found.

### List of original Dockerfiles.
1. [Jupyter scipy notebook](https://github.com/jupyter/docker-stacks/blob/main/images/scipy-notebook/Dockerfile)
2. [Jupyter minimal-notebook](https://github.com/jupyter/docker-stacks/blob/main/images/minimal-notebook/Dockerfile)
3. [Jupyter base-notebook](https://github.com/jupyter/docker-stacks/blob/main/images/base-notebook/Dockerfile)
4. [Jupyter foundation notebook](https://github.com/jupyter/docker-stacks/blob/main/images/docker-stacks-foundation/Dockerfile)
