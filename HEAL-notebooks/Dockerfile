FROM quay.io/cdis/jupyter-superslim-r:3.1.0

# To build locally, specify the Dockerfile and the notebook subdirectory.
# For example, run this in the HEAL-notebooks directory:
#   docker build -t some_tag -f Dockerfile generic_rkernel

USER $NB_USER
ARG NOTEBOOK_DIR

# Available files are limited to notebook subdirectory
COPY . $HOME/

# clean things up
USER root
RUN if [ -d $HOME/img ]; then rm -rf $HOME/img; fi
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
