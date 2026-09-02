FROM quay.io/cdis/jupyterlab-generic:master

# Included for clarity
COPY jupyterlab-start.sh .
RUN chmod +x jupyterlab-start.sh && \
    chown ${NB_USER}:${NB_USER} /jupyterlab-start.sh

USER $NB_USER

COPY heal-software-library-welcome.ipynb $HOME/

CMD ["/jupyterlab-start.sh"]
