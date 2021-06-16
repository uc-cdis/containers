FROM quay.io/cdis/jupyter-notebook:1.1.0

USER $NB_USER
WORKDIR /home/$NB_USER

COPY ./resources/requirements.txt ${HOME}/

COPY ./resources/HEAL_Workspace_Demo_BACPAC.ipynb ${HOME}/

RUN pip install -r ${HOME}/requirements.txt
