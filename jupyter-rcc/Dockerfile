# 1. Base the image on official Python 3.14
FROM python:3.14-slim

USER root

# 2. Install essential system build toolchains and dependencies
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

# 3. Create the 'jovyan' user context required by Gen3 workspaces
RUN useradd -m -s /bin/bash jovyan
ENV HOME=/home/jovyan
WORKDIR $HOME

# 4. Copy requirements and compile Python packages under Python 3.14
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --no-cache-dir -r requirements.txt

# 5. Install GRCh38 genome reference
RUN python3 -c "from SigProfilerMatrixGenerator import install as genInstall; genInstall.install('GRCh38', rsync=False, bash=True)"

# Fix ownership rights for the user runtime
RUN chown -R jovyan:jovyan $HOME

# 6. Expose standard Jupyter runtime port for Gen3 proxy routing
EXPOSE 8888

# Switch to the secure non-root context
USER jovyan

# 7. Start Jupyter Lab when the Gen3 workspace pod initializes
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--AllowRoot=False"]
