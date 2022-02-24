FROM jupyter/datascience-notebook:notebook-6.4.8
USER root

USER $NB_UID

WORKDIR /home/$NB_USER

COPY --chown=jovyan:users resources/custom.js /home/$NB_USER/.jupyter/custom/
COPY --chown=jovyan:users resources/jupyter_notebook_config.py /home/$NB_USER/.jupyter/
