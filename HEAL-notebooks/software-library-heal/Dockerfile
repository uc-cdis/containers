FROM quay.io/cdis/jupyterlab-generic:master

USER $NB_USER

# Welcome notebook for this container
COPY heal-welcome-wsl.ipynb $HOME/

# packages for welcome notebook that are not in jupyterlab-generic
RUN python3.14 -m pip install --user ipywidgets

# the start script comes from jupyterlab-generic
CMD ["/jupyterlab-start.sh"]
