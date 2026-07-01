# Base the image on official Python 3.14
FROM python:3.14-slim

USER root

# Install essential system build toolchains, dependencies, and git CLI tools
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
# CREATE A STARTUP WRAPPER SCRIPT
# This script acts as a traffic controller whenever the container initializes.
# It prepares the user environment and decides whether to launch JupyterLab
# or run custom commands (like /bin/bash for local tests).
# =========================================================================
RUN echo '#!/bin/bash\n\
# -------------------------------------------------------------------------\n\
# STEP 1: RESTORE TERMINAL ENVIRONMENT & AUTOCOMPLETION\n\
# When Gen3 mounts persistent volumes, home profiles can sometimes be missing.\n\
# If .bashrc does not exist, copy the default system templates from /etc/skel.\n\
# This fixes the broken terminal prompt, restoring username, host, and tab-autocomplete.\n\
# -------------------------------------------------------------------------\n\
if [ ! -f "/home/jovyan/.bashrc" ]; then \n\
    cp /etc/skel/.bash* /home/jovyan/ 2>/dev/null || true; \n\
fi\n\
\n\
# -------------------------------------------------------------------------\n\
# STEP 2: SANITIZE KUBERNETES / GEN3 STORAGE ARGUMENTS\n\
# Some cluster orchestrators append the name of this script to the argument list.\n\
# If the first argument ($1) is "start-notebook.sh", remove it ("shift") \n\
# so it does not get passed to Jupyter and cause a startup flag error.\n\
# -------------------------------------------------------------------------\n\
if [ "$1" = "start-notebook.sh" ]; then \n\
    shift; \n\
fi\n\
\n\
# -------------------------------------------------------------------------\n\
# STEP 3: DETECT RUNTIME MODE (PRODUCTION VS LOCAL TESTING)\n\
# We check if there are zero arguments ($# -eq 0) OR if the first argument \n\
# looks like a Jupyter configuration flag (starts with "--", like --ip=0.0.0.0).\n\
# -------------------------------------------------------------------------\n\
if [ $# -eq 0 ] || [[ "$1" == --* ]]; then\n\
    # MODE A: PRODUCTION MODE (Gen3 Environment)\n\
    # Launch the JupyterLab server app and seamlessly inject all the \n\
    # system flags ("$@") provided by the Gen3 Hatchery configuration block.\n\
    exec jupyter lab "$@"\n\
else\n\
    # MODE B: TESTING MODE (Local Desktop / Manual Debugging)\n\
    # If the user passed a direct command (like /bin/bash or python3 script.py),\n\
    # bypass Jupyter entirely and execute the user command directly instead.\n\
    exec "$@"\n\
fi' > /usr/local/bin/start-notebook.sh && \
    # -------------------------------------------------------------------------\n\
    # STEP 4: AUTHORIZE SCRIPT EXECUTION\n\
    # Grant executable permissions (+x) to the script. Without this line,\n\
    # Linux will block the container from running it, causing a crash.\n\
    # -------------------------------------------------------------------------\n\
    chmod +x /usr/local/bin/start-notebook.sh

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
