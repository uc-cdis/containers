FROM quay.io/cdis/jupyterlab-generic@sha256:159cf4b861995089e9c3c1f7f5e93ef2d90a59f857008ba79e3c230ef5dff56a

USER $NB_USER

# Welcome notebook for this container
COPY heal-welcome-wsl.ipynb $HOME/

# packages for welcome notebook that are not in jupyterlab-generic
RUN python3.14 -m pip install --user ipywidgets

# the start script comes from jupyterlab-generic
CMD ["/jupyterlab-start.sh"]
