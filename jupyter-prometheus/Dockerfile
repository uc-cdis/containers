FROM quay.io/cdis/jupyterlab-generic:master

USER root

# Install system dependencies
RUN dnf update -y && dnf install -y \
    gcc-c++ \
    ghostscript-devel \
    gsl-devel \
    gzip \
    libcurl-devel \
    libssh2-devel \
    libxml2-devel \
    openssl \
    openssl-devel \
    python3.14 \
    python3.14-pip \
    python3.14-setuptools \
    python3.14-pip-wheel \
    tar \
    unzip \
    wget \
    zlib-devel \
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

USER jovyan

# Install everything from requirements.txt
COPY requirements.txt .
RUN pip3.14 install --no-cache-dir -r requirements.txt

# Copy notebook directory
COPY combined_demos/ $HOME/

# Add virtual environment function to bashrc
RUN echo 'function ve(){ mkdir -p virtualenv; cd virtualenv; VENV="$1"; python3.14 -m venv $VENV --system-site-packages; source $VENV/bin/activate; python3.14 -m ipykernel install --user --name=$VENV; deactivate; }' >> /home/jovyan/.bashrc

# WORKDIR $HOME
