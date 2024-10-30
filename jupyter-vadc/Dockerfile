FROM quay.io/cdis/datascience-notebook:2024-02-26

USER root

# this is absolutely necessary for pymssql
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        freetds-bin \
    && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}

# install from the requirements.txt file
COPY --chown=${NB_UID}:${NB_GID} resources/requirements.txt /tmp/requirements.txt
RUN mamba install --yes --file /tmp/requirements.txt && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

WORKDIR /home/${NB_USER}

COPY --chown=jovyan:users resources/custom.js /home/${NB_USER}/.jupyter/custom/
COPY --chown=jovyan:users resources/jupyter_notebook_config.py /home/${NB_USER}/.jupyter/
