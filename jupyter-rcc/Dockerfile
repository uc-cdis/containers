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

# Define custom reference genome storage directory path
ENV SIGPROFILERMATRIXGENERATOR_VOLUME="/home/jovyan/shared_genomes"
RUN mkdir -p /home/jovyan/shared_genomes && chown -R jovyan:jovyan /home/jovyan

# Add user binary paths to environment PATH so CLI commands execute globally
ENV PATH="/home/jovyan/.local/bin:${PATH}"

# Switch to secure user context early to enforce user execution ownership
USER jovyan

# Copy requirements and compile packages
COPY requirements.txt .
RUN pip3 install --user --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --user --no-cache-dir -r requirements.txt

# Pre-download and cache genomic index sequences natively using the CLI interface
# This saves the files directly to  the custom /home/jovyan/shared_genomes path
RUN SigProfilerMatrixGenerator install GRCh38

# Expose standard Jupyter runtime port for Gen3 proxy routing
EXPOSE 8888

# Start Jupyter Lab when the Gen3 workspace pod initializes
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--AllowRoot=False"]
