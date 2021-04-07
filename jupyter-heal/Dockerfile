FROM quay.io/cdis/jupyter-notebook:1.1.0

USER $NB_USER
WORKDIR /home/$NB_USER

COPY ./resources/requirements.txt ${HOME}/

# copy premade notebooks
COPY ./resources/*.ipynb ${HOME}/

# premade notebooks dependencies
RUN pip install -r ${HOME}/requirements.txt
