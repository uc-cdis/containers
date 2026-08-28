FROM public.ecr.aws/u5x5h6w3/nextflow-approved/public:gen3-cuda-12.3-ubuntu22.04-openssl

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies + clean up
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        python3-pip \
        python3-dev \
        python3-opencv \
        libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*
# Upgrade pip and install torch (NO CACHE)
RUN python3 -m pip install --upgrade pip && \
    pip3 install --no-cache-dir torch \
        -f https://download.pytorch.org/whl/cu123/torch_stable.html

# Set the working directory
WORKDIR /app

# Set the entrypoint
ENTRYPOINT [ "python3" ]
