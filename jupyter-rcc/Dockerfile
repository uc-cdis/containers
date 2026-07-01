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
# IMPORT AND AUTHORIZE THE STARTUP WRAPPER SCRIPT
# Copy the script into a global system directory path and make it executable
# =========================================================================
COPY start-notebook.sh /usr/local/bin/start-notebook.sh
RUN chmod +x /usr/local/bin/start-notebook.sh

# Switch to the secure Gen3 user context permanently for all subsequent build steps
USER jovyan

# Copy requirements and compile packages
COPY requirements.txt .
RUN pip3 install --user --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --user --no-cache-dir -r requirements.txt

# Pre-download genomes directly into the safe internal home directory path
ENV SIGPROFILERMATRIXGENERATOR_VOLUME="/home/jovyan/reference_genomes"
RUN SigProfilerMatrixGenerator install GRCh38 && \
    SigProfilerMatrixGenerator install GRCh37


# Force JupyterLab terminal interface to spawn full Bash shell sessions instead of basic /bin/sh
ENV SHELL="/bin/bash"

# Expose standard Jupyter runtime port for Gen3 proxy routing
EXPOSE 8888

# Start notebook using standard entrypoint form to properly inherit Gen3 command/args array
ENTRYPOINT ["start-notebook.sh"]
