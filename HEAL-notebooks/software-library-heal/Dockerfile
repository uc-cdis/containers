FROM quay.io/cdis/jupyterlab-generic:master

USER $NB_USER

# Welcome notebook for this container
COPY heal-welcome-wsl.ipynb $HOME/

# the start script comes from jupyterlab-generic
CMD ["/jupyterlab-start.sh"]
