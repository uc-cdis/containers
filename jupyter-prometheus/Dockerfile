FROM quay.io/cdis/jupyter-superslim-r:1.0.4

ARG NOTEBOOK_DIR

COPY $NOTEBOOK_DIR/ $HOME/
USER root
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
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip uninstall -y gen3
RUN pip3 install gen3
RUN pip3 install pandas
RUN pip3 install seaborn
RUN pip3 install matplotlib
RUN pip3 install scipy

RUN printf '\n\
if [ -f $HOME/requirements.txt ]; then \n\
    echo "Will install requirements.txt" \n\
    conda install --file $HOME/requirements.txt \n\
    rm $HOME/requirements.txt \n\
else \n\
    echo "No dependencies to install." \n\
fi \n\
' | bash

RUN echo 'function ve(){ mkdir virtualenv; cd virtualenv; VENV="$1"; python3 -m venv $VENV --system-site-packages; source $VENV/bin/activate; python -m ipykernel install --user --name=$VENV; deactivate;}' >> ~/.bashrc