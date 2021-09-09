FROM quay.io/cdis/jupyter-notebook:1.1.0

USER $NB_USER
WORKDIR /home/$NB_USER

COPY ./resources/requirements.txt ${HOME}/

COPY ./resources/JCOIN_Tracking_Opioid_Stigma.ipynb ${HOME}/

RUN pip install -r ${HOME}/requirements.txt
