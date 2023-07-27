FROM quay.io/cdis/jupyter-pystata-user-licensed:feat_stata-license

USER root
RUN apt-get update
RUN apt-get install -y firefox
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN mv geckodriver /bin/

COPY jupyter-pystata-licensed/resources/wait_for_license.sh /tmp/
COPY jupyter-pystata-licensed/resources/setup_licensed_notebook.py /tmp/
RUN chmod 777 /tmp/wait_for_license.sh /tmp/setup_licensed_notebook.py

USER $NB_USER
RUN pip3 install selenium

# Pin stata_setup to avoid error on splash parameter
RUN pip3 uninstall --yes stata-setup
RUN pip3 install stata-setup==0.1.2

# Remove the notebook created in jupyter-pystata-user-licensed
RUN rm $HOME/Stata.ipynb
COPY jupyter-pystata-licensed/resources/licensed_stata_session.ipynb $HOME
