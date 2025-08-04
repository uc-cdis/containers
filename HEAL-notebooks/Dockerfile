FROM quay.io/cdis/jupyter-superslim-r:fix_al2

USER $NB_USER
ARG NOTEBOOK_DIR

COPY $NOTEBOOK_DIR/ $HOME/

RUN pip3 install healdata-utils
RUN pip3 install gen3
RUN pip3 install heal-sdk
RUN conda config --append channels conda-forge
RUN conda install -c plotly plotly


RUN printf '\n\
if [ -f $HOME/requirements.txt ]; then \n\
    echo "Will install requirements.txt" \n\
    conda install --file $HOME/requirements.txt \n\
    rm $HOME/requirements.txt \n\
else \n\
    echo "No dependencies to install." \n\
fi \n\
' | bash
