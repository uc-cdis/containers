FROM jupyter/minimal-notebook

ARG NOTEBOOK_DIR

COPY $NOTEBOOK_DIR/ $HOME/

RUN printf '\n\
if [ -f $HOME/requirements.txt ]; then \n\
    echo "Will install requirements.txt" \n\
    pip install -r $HOME/requirements.txt \n\
    rm $HOME/requirements.txt \n\
else \n\
    echo "No dependencies to install." \n\
fi \n\
' | bash
