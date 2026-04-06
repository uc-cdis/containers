# Generic Gen3 JupyterLab workspace

FROM public.ecr.aws/amazonlinux/amazonlinux:2023-minimal
LABEL maintainer="Center for Translational Data Science (CTDS)"
LABEL name="jupyterlab-generic"

# TODO: git, nodejs, and build are all required only to build jupyterlmod;
#       these can be dropped once jupyterlmod fix is available in PyPI.
RUN dnf upgrade --refresh && \
    dnf install -y python3.14 python3.14-pip git nodejs shadow-utils which && \
    python3.14 -m venv /usr/local/python-venv && \
    source /usr/local/python-venv/bin/activate && \
    pip install --upgrade pip && \
    pip install jupyterlab && \
    pip install build && \
    pip install jupyterlmod git+https://github.com/pschumm/jupyter-lmod@pschumm/fix_hidden && \
    pip install jupyterlab-git && \
    pip install jupyterlab-search-replace && \
    pip install ipykernel==6.31.0 && \
    python3.14 -m ipykernel install --name "Python-3.14.0" --display-name "Python 3.14 (ipykernel)"

RUN ln -s /usr/bin/python3.14 /usr/bin/python3 && \
    ln -s /usr/bin/python3.14 /usr/bin/python

RUN /usr/local/python-venv/bin/jupyter kernelspec remove -y python3

# This is needed for running stata_setup
RUN dnf -y update
RUN dnf install -y \
	ncurses-compat-libs \
	gzip \
	tar && \
    dnf clean all

COPY jupyterlab-start.sh .
RUN chmod +x jupyterlab-start.sh

EXPOSE 8888

# Create home directory manually to avoid copying skeleton files
RUN groupadd -g 1010 jovyan && \
    useradd -u 1010 -g jovyan -M jovyan && \
    mkdir /home/jovyan && \
    chown jovyan:jovyan /home/jovyan && \
    chmod 700 /home/jovyan && \
    usermod -d /home/jovyan jovyan && \
    usermod --shell /bin/bash jovyan
USER jovyan
WORKDIR /home/jovyan

# Enable lmod
ENV LMOD_CMD=/apps/lmod/lmod/libexec/lmod
ENV MODULEPATH=/apps/lmod/lmod/modulefiles
ENV LMOD_MODULERC=/apps/lmod/lmod/.modulerc.lua

# Make sure bash is the default shell within JupyterLab terminal
ENV SHELL=/bin/bash

CMD ["/jupyterlab-start.sh"]
