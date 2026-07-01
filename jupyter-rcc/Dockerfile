# Base the image on official Python 3.14
FROM python:3.14-slim

USER root

# Install essential system build toolchains, dependencies, git, and curl
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    libxml2-dev \
    libssl-dev \
    libcurl4-openssl-dev \
    libssh2-1-dev \
    zlib1g-dev \
    libgsl-dev \
    ghostscript \
    unzip \
    wget \
    tar \
    gzip \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# For Gen3 workspaces create the jovyan group with GID 101, then create user jovyan with UID 1010 and group name jovyan
RUN groupadd -g 101 jovyan && \
    useradd -m -s /bin/bash -u 1010 -g jovyan jovyan

ENV HOME=/home/jovyan
WORKDIR $HOME

# Setup default placeholder directories and fix base permissions
RUN mkdir -p /home/jovyan/pd && chown -R jovyan:jovyan /home/jovyan

# Add user binary paths to environment PATH so CLI commands execute globally
ENV PATH="/home/jovyan/.local/bin:${PATH}"

# =========================================================================
# SYSTEM STARTUP WRAPPER ASSEMBLY
# This block creates and registers /usr/local/bin/start-notebook.sh.
# 1) It copies basic skeletal files (.bashrc) if missing to fix the prompt.
# 2) It shifts away redundant script name arguments added by Kubernetes.
# 3) It routes execution to JupyterLab or passes manual testing commands.
# =========================================================================
RUN echo '#!/bin/bash\n\
if [ ! -f "/home/jovyan/.bashrc" ]; then \n\
    cp /etc/skel/.bash* /home/jovyan/ 2>/dev/null || true; \n\
fi\n\
if [ "$1" = "start-notebook.sh" ]; then \n\
    shift; \n\
fi\n\
if [ $# -eq 0 ] || [[ "$1" == --* ]]; then\n\
    exec jupyter lab "$@"\n\
else\n\
    exec "$@"\n\
fi' > /usr/local/bin/start-notebook.sh && chmod +x /usr/local/bin/start-notebook.sh

# Switch to the secure Gen3 user context permanently for all subsequent build steps
USER jovyan

# Copy requirements and compile packages
COPY requirements.txt .
RUN pip3 install --user --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --user --no-cache-dir -r requirements.txt

# Pre-download genomes directly into the safe internal home directory path
ENV SIGPROFILERMATRIXGENERATOR_VOLUME="/home/jovyan/reference_genomes"
RUN SigProfilerMatrixGenerator install GRCh38

# Force JupyterLab terminal interface to spawn full Bash shell sessions instead of basic /bin/sh
ENV SHELL="/bin/bash"

# Expose standard Jupyter runtime port for Gen3 proxy routing
EXPOSE 8888

# Start notebook using standard entrypoint form to properly inherit Gen3 command/args array
ENTRYPOINT ["start-notebook.sh"]
