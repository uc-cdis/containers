FROM quay.io/cdis/jupyter-superslim-r:2.0.0

ARG NOTEBOOK_DIR

COPY $NOTEBOOK_DIR/ $HOME/

RUN pip3 install healdata-utils
RUN pip3 install gen3==4.25.1 # Pinning older gen3sdk for now while conflict is resolved
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
