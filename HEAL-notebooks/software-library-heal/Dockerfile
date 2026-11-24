FROM quay.io/cdis/jupyterlab-generic@sha256:b4033fee8ca9c1c60e4603641c679d6b4c5071e07dd2637c4126e4cd11917ce5

USER $NB_USER

# Welcome notebook for this container
COPY heal-welcome-wsl.ipynb $HOME/

# packages for welcome notebook that are not in jupyterlab-generic
RUN python3.14 -m pip install --user ipywidgets

# the start script comes from jupyterlab-generic
CMD ["/jupyterlab-start.sh"]
