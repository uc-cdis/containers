FROM quay.io/cdis/datascience-notebook:2023-04-10

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        freetds-bin \
    && rm -rf /var/lib/apt/lists/*

USER ${NB_UID}

# install extra packages
RUN mamba install --quiet --yes \
    'pymssql' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

WORKDIR /home/${NB_USER}

COPY --chown=jovyan:users resources/custom.js /home/${NB_USER}/.jupyter/custom/
COPY --chown=jovyan:users resources/jupyter_notebook_config.py /home/${NB_USER}/.jupyter/
