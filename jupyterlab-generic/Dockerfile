# Generic Gen3 JupyterLab workspace

FROM public.ecr.aws/amazonlinux/amazonlinux:2023-minimal
LABEL maintainer="Center for Translational Data Science (CTDS)"
LABEL name="jupyterlab-generic"

# Configure environment for NB_USER since we are using generic amazonlinux base image
# similar to https://github.com/uc-cdis/jupyter-superslim/Dockerfile
ARG NB_USER="jovyan"
ARG NB_UID="1010"
ARG NB_GID="1010"
ENV NB_USER="${NB_USER}" \
    NB_UID="${NB_UID}" \
    NB_GID="${NB_GID}" \
    HOME="/home/${NB_USER}"



# TODO: git, nodejs, and build are all required only to build jupyterlmod;
#       these can be dropped once jupyterlmod fix is available in PyPI.
RUN dnf upgrade --refresh && \
    dnf install -y python3.14 python3.14-pip git \
        shadow-utils which ca-certificates && \
    curl -fsSL https://rpm.nodesource.com/setup_20.x | bash - && \
    dnf install -y nodejs

# Create home directory manually to avoid copying skeleton files
# TODO: change this to env var (see below)
# RUN groupadd -g 1010 jovyan && \
#     useradd -u 1010 -g jovyan -M jovyan && \
#     mkdir /home/jovyan && \
#     chown jovyan:jovyan /home/jovyan && \
#     chmod 700 /home/jovyan && \
#     usermod -d /home/jovyan jovyan && \
#     usermod --shell /bin/bash jovyan

# USER ${NB_USER}
# WORKDIR /home/jovyan
# RUN echo "NB_USER is $NB_USER"

RUN python3.14 -m pip install --upgrade pip setuptools wheel && \
    python3.14 -m pip install \
        jupyterlab \
        build && \
    python3.14 -m pip install \
        jupyterlmod \
        git+https://github.com/pschumm/jupyter-lmod@pschumm/fix_hidden && \
    python3.14 -m pip install jupyterlab-git \
        jupyterlab-search-replace \
        ipykernel==6.31.0 && \
    python3.14 -m ipykernel install \
        --name "Python-3.14.0" \
        --display-name "Python 3.14 (ipykernel)" && \
    dnf clean all

RUN which jupyter
# Switch back to root for system level things
USER root
RUN ln -s /usr/bin/python3.14 /usr/local/bin/python3 && \
    ln -s /usr/bin/python3.14 /usr/local/bin/python

    # Create non-root user
RUN groupadd -g ${NB_GID} ${NB_USER} && \
    useradd -u ${NB_UID} -g ${NB_USER} -M ${NB_USER} && \
    mkdir -p ${HOME} && \
    chown ${NB_USER}:${NB_USER} ${HOME} && \
    chmod 700 ${HOME} && \
    usermod -d ${HOME} ${NB_USER} && \
    usermod --shell /bin/bash ${NB_USER}

COPY jupyterlab-start.sh .
RUN chmod +x jupyterlab-start.sh && \
    chown ${NB_USER}:${NB_USER} /jupyterlab-start.sh

EXPOSE 8888

USER ${NB_USER}
WORKDIR ${HOME}
RUN echo "NB_USER is $NB_USER"

# Enable lmod
ENV LMOD_CMD=/apps/lmod/lmod/libexec/lmod
ENV MODULEPATH=/apps/lmod/lmod/modulefiles
ENV LMOD_MODULERC=/apps/lmod/lmod/.modulerc.lua

# Make sure bash is the default shell within JupyterLab terminal
ENV SHELL=/bin/bash

# Add user binary paths to environment PATH so CLI commands execute globally
ENV PATH="/home/jovyan/.local/bin:${PATH}"
# Add the user path to PYTHONPATH for user installed modules
# ENV PYTHONPATH="/home/jovyan/.local/lib/python3.14/site-packages:${PYTHONPATH}"

CMD ["/jupyterlab-start.sh"]
