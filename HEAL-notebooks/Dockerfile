FROM quay.io/cdis/jupyter-superslim-r:3.0.0

USER $NB_USER
ARG NOTEBOOK_DIR

COPY $NOTEBOOK_DIR/ $HOME/

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
