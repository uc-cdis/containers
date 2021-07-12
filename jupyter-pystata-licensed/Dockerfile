FROM quay.io/cdis/stata-heal:master

USER root
RUN apt-get update
RUN apt-get install -y firefox
RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.29.1/geckodriver-v0.29.1-linux64.tar.gz
RUN tar -xvzf geckodriver*
RUN mv geckodriver /bin/
RUN rm geckodriver*

COPY jupyter-pystata-licensed/resources/wait_for_license.sh /tmp/
COPY jupyter-pystata-licensed/resources/init_licensed_stata_notebook.py /tmp/
RUN chmod 777 /tmp/wait_for_license.sh /tmp/init_licensed_stata_notebook.py

USER $NB_USER
RUN pip3 install selenium
