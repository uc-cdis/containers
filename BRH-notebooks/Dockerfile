FROM quay.io/cdis/jupyter-superslim-r:1.0.0

ARG NOTEBOOK_DIR

COPY $NOTEBOOK_DIR/ $HOME/

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
