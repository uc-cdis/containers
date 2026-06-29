# Base the image on official Python 3.14
FROM python:3.14-slim

USER root

# Install essential system build toolchains and dependencies
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
    && rm -rf /var/lib/apt/lists/*

# Create the secure jovyan user context required by Gen3 workspaces
RUN useradd -m -s /bin/bash jovyan
ENV HOME=/home/jovyan
WORKDIR $HOME

# Copy requirements and compile packages directly under Python 3.14
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt

# Install reference genome GRCh38
RUN python3 -c "from SigProfilerMatrixGenerator import install as gen; gen.install('GRCh38', rsync=False, bash=True)"

# Fix directory ownership rights for the jovyan user runtime
RUN chown -R jovyan:jovyan $HOME

# Expose standard Jupyter runtime port for Gen3 proxy routing
EXPOSE 8888

# Switch to the secure non-root context
USER jovyan

# Start Jupyter Lab when the Gen3 workspace pod initializes
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--AllowRoot=False"]
