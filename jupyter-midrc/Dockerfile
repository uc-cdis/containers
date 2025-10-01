FROM quay.io/cdis/jupyter-superslim-r:1.0.4

WORKDIR /home/jovyan

# Copy your notebooks and requirements.txt into the container
COPY combined_demos/ /home/jovyan/
COPY requirements.txt /home/jovyan/

USER root

# Install system and dev dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    python3 \
    python3-pip \
    g++ \
    libxml2-dev \
    libssl-dev \
    libcurl4-openssl-dev \
    libssh2-1-dev \
    zlib1g-dev \
    openssl \
    gdebi-core \
    libgsl* \
    libudunits2-dev \
    libgs-dev \
    unzip \
    wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages from requirements.txt
RUN pip3 install --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt && \
    rm requirements.txt

USER jovyan

CMD ["start-notebook.sh"]
