FROM quay.io/cdis/jupyter-notebook:1.0.1

USER $NB_UID

## Append custom settings to jupyter config file
COPY jupyter_notebook_config.py /home/$NB_USER/.jupyter/tmp.py
RUN cat /home/$NB_USER/.jupyter/tmp.py >> /home/$NB_USER/.jupyter/jupyter_notebook_config.py && rm /home/$NB_USER/.jupyter/tmp.py
