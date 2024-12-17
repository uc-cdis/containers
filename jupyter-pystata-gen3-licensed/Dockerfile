FROM quay.io/cdis/jupyter-pystata-user-licensed:feat_stata-base-update

USER root
RUN apt-get update
RUN apt-get install -y firefox
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.34.0/geckodriver-v0.34.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN mv geckodriver /bin/

COPY jupyter-pystata-gen3-licensed/resources/wait_for_license.sh /tmp/
COPY jupyter-pystata-gen3-licensed/resources/setup_licensed_notebook.py /tmp/
RUN chmod 777 /tmp/wait_for_license.sh /tmp/setup_licensed_notebook.py

USER $NB_USER
RUN pip3 install selenium

RUN pip3 uninstall --yes stata-setup
RUN pip3 install stata-setup

# Remove the notebook created in jupyter-pystata-user-licensed
RUN rm $HOME/Stata.ipynb
COPY jupyter-pystata-gen3-licensed/resources/licensed_stata_session.ipynb $HOME
