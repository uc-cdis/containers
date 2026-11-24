FROM quay.io/cdis/jupyterlab-generic@sha256:0976b0227a38ffc6d6b0c327d7e4e8cdb2a06fd1052da57d449a9ddacdc3ae62

USER $NB_USER

# Welcome notebook for this container
COPY heal-welcome-wsl.ipynb $HOME/

# packages for welcome notebook that are not in jupyterlab-generic
RUN python3.14 -m pip install --user ipywidgets

# the start script comes from jupyterlab-generic
CMD ["/jupyterlab-start.sh"]
