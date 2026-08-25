# Use the amazonlinux-base image as the base
FROM quay.io/cdis/amazonlinux-base

# Install kubectl
RUN curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x kubectl && \
    mv kubectl /usr/local/bin/

# Verify installations
RUN curl --version && kubectl version --client

# Set working directory
WORKDIR /app

# Default command
CMD ["/bin/bash"]
