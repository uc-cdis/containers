FROM quay.io/cdis/jupyter-superslim:1.0.1

USER root
RUN apt-get update

# needed if user wants to run stinit (license validation) in the workspace
RUN	apt-get install -y libncurses5

RUN mkdir /usr/local/stata17
COPY jupyter-pystata-user-licensed/resources/Stata17Linux64.tar.gz /tmp/Stata17Linux64.tar.gz
RUN cd /usr/local/stata17 && tar -xvf /tmp/Stata17Linux64.tar.gz

RUN chown $NB_USER /usr/local/stata17/
ENV PATH $PATH:/usr/local/stata17
RUN cd /usr/local/stata17 && \
	{ echo y; echo y; echo y; } | ./install

# COPY jupyter-pystata/resources/Stata.ipynb Stata-1.ipynb
# COPY jupyter-pystata/resources/Stata.ipynb Stata-2.ipynb
# COPY jupyter-pystata/resources/Stata.ipynb Stata-3.ipynb
# COPY jupyter-pystata/resources/Stata.ipynb Stata-4.ipynb
# COPY jupyter-pystata/resources/Stata.ipynb Stata-5.ipynb
# COPY jupyter-pystata/resources/welcome.html .

USER $NB_USER
RUN pip install --user stata_setup

COPY jupyter-pystata/dockerstart.sh /usr/local/bin/

# USER root
# RUN apt-get update
# RUN apt-get install -y firefox
# RUN wget https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
# RUN tar -xvzf geckodriver*.tar.gz
# RUN mv geckodriver /bin/
# RUN rm geckodriver*.tar.gz

# COPY jupyter-pystata-user-licensed/resources/setup_notebooks.py /tmp/

# USER $NB_USER
# RUN pip3 install selenium

# RUN mkdir /tmp/custom_api
# COPY jupyter-pystata-user-licensed/resources/custom_api/* /tmp/custom_api/
# ENV PYTHONPATH="${PYTHONPATH}:/tmp/"

# CMD /usr/local/bin/dockerstart.sh
