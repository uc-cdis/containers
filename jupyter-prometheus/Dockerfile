FROM quay.io/cdis/jupyter-superslim-r:2.1.0

ARG NOTEBOOK_DIR

USER root

# Install system dependencies
RUN dnf update -y && dnf install -y \
    # curl \
    python3 \
    python3-pip \
    gcc-c++ \
    libxml2-devel \
    openssl-devel \
    libcurl-devel \
    libssh2-devel \
    zlib-devel \
    openssl \
    gsl-devel \
    ghostscript-devel \
    unzip \
    wget \
    tar \
    gzip \
    shadow-utils \
    && dnf clean all

# Install udunits2 from source since it's not in AL2023 repos
# RUN wget -q https://artifacts.unidata.ucar.edu/repository/downloads-udunits/2.2.28/udunits-2.2.28.tar.gz && \
#     tar -xzf udunits-2.2.28.tar.gz && \
#     cd udunits-2.2.28 && \
#     ./configure --prefix=/usr/local && \
#     make && make install && \
#     cd .. && rm -rf udunits-2.2.28* && \
#     echo "/usr/local/lib" >> /etc/ld.so.conf.d/udunits2.conf && \
#     ldconfig

# Create user and home directory if they don't exist
RUN if ! id -u jovyan >/dev/null 2>&1; then \
        useradd -m -s /bin/bash jovyan; \
    fi

# Set HOME variable
ENV HOME=/home/jovyan

# Copy notebook directory
COPY $NOTEBOOK_DIR/ $HOME/

# Switch to root for installations
USER root

# Uninstall gen3 if preinstalled
RUN pip3 uninstall -y gen3 || true

# Install everything from requirements.txt
COPY requirements.txt .
# RUN pip3 install --no-cache-dir -r requirements.txt


# Install conda (miniconda) for AL2023
# RUN wget -q https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /tmp/miniconda.sh && \
#     bash /tmp/miniconda.sh -b -p /opt/conda && \
#     rm /tmp/miniconda.sh && \
#     /opt/conda/bin/conda clean -afy

# Add conda to PATH
ENV PATH="/opt/conda/bin:${PATH}"

# Handle requirements.txt if present
RUN if [ -f $HOME/requirements.txt ]; then \
        echo "Will install requirements.txt"; \
        /opt/conda/bin/conda install --file $HOME/requirements.txt || \
        pip3 install -r $HOME/requirements.txt; \
        rm $HOME/requirements.txt; \
    else \
        echo "No dependencies to install."; \
    fi

# Add virtual environment function to bashrc
RUN echo 'function ve(){ mkdir -p virtualenv; cd virtualenv; VENV="$1"; python3 -m venv $VENV --system-site-packages; source $VENV/bin/activate; python -m ipykernel install --user --name=$VENV; deactivate;}' >> /home/jovyan/.bashrc

# Fix ownership
RUN chown -R jovyan $HOME

# Switch to non-root user
USER jovyan

WORKDIR $HOME
