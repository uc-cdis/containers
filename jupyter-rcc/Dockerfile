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

# Add the user local binary path to environment PATH so CLI tools work out-of-the-box
ENV PATH="/home/jovyan/.local/bin:${PATH}"

# Switch to the secure non-root context early to ensure native user ownership
USER jovyan

# Copy requirements and compile packages directly into the jovyan home directory
COPY requirements.txt .
RUN pip3 install --user --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --user --no-cache-dir -r requirements.txt

# Pre-download and cache genomic index sequences natively using the CLI interface
RUN SigProfilerMatrixGenerator install GRCh38

# Create the missing validation marker file to fix the library's internal status bug
RUN touch /home/jovyan/.local/lib/python3.14/site-packages/SigProfilerMatrixGenerator/references/chromosomes/tsb/GRCh38/RefGen_Ver.txt

# Expose standard Jupyter runtime port for Gen3 proxy routing
EXPOSE 8888

# Start Jupyter Lab when the Gen3 workspace pod initializes
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--AllowRoot=False"]
