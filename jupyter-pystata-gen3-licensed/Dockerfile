FROM quay.io/cdis/jupyter-pystata-user-licensed:3.1.1

USER root
RUN yum install -y firefox jq
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.36.0/geckodriver-v0.36.0-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN mv geckodriver /bin/

COPY ./resources/wait_for_license.sh /tmp/
COPY ./resources/setup_licensed_notebook.py /tmp/
RUN chmod 777 /tmp/wait_for_license.sh /tmp/setup_licensed_notebook.py

COPY ./resources/licensed_stata_session.ipynb $HOME
RUN chown "${NB_USER}:${NB_GID}" $HOME/licensed_stata_session.ipynb

USER $NB_USER
RUN pip3 install selenium

RUN pip3 uninstall --yes stata-setup
RUN pip3 install stata-setup

# Remove the notebook created in jupyter-pystata-user-licensed
RUN rm $HOME/Stata.ipynb
