FROM quay.io/cdis/jupyter-superslim-r:3.1.0

# To build locally, run this in the HEAL-notebooks/generic_rkernel directory:
#   docker build -t some_tag .

# Make the base image's start-notebook.sh launch `jupyter lab` instead of `jupyter notebook`
ENV JUPYTER_ENABLE_LAB=1

USER $NB_USER
ARG NOTEBOOK_DIR

# Available files are limited to this directory (the build context).
# COPY creates files as root regardless of USER, so chown them to the notebook user
# so that notebooks can be edited and saved.
COPY --chown=${NB_UID}:${NB_GID} . $HOME/

# clean things up
USER root
RUN rm -rf $HOME/img $HOME/Dockerfile
USER $NB_USER

RUN conda config --append channels conda-forge
RUN conda install --quiet --yes -c conda-forge nodejs


RUN printf '\n\
if [[ -f $HOME/pyproject.toml && -f $HOME/poetry.lock ]]; then \n\
    echo "Will install packages using Poetry" \n\
    poetry config virtualenvs.create false \n \
    poetry install -vv --no-interaction \n\
    rm $HOME/pyproject.toml $HOME/poetry.lock \n\
else \n\
    echo "No packages to install." \n\
fi \n\
' | bash
