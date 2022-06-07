FROM quay.io/cdis/jupyter-superslim-r:master

ARG NOTEBOOK_DIR

COPY $NOTEBOOK_DIR/ $HOME/
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    python3 \
    python3-pip \
    g++ \
    wget && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN conda config --append channels conda-forge
RUN conda config --add channels bioconda
RUN conda install -c plotly plotly
RUN conda update conda --all
RUN conda install -c bioconda bioconductor-gdcrnatools


RUN printf '\n\
    if [ -f $HOME/requirements.txt ]; then \n\
    echo "Will install requirements.txt" \n\
    conda install --file $HOME/requirements.txt \n\
    rm $HOME/requirements.txt \n\
    else \n\
    echo "No dependencies to install." \n\
    fi \n\
    ' | bash
