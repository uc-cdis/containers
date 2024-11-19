FROM quay.io/cdis/jupyter-superslim:2.0.0

USER root
RUN apt-get update

# needed if user wants to run stinit (license validation) in the workspace
RUN	apt-get install -y libncurses5

RUN mkdir /usr/local/stata17
COPY ./resources/Stata17Linux64.tar.gz /tmp/Stata17Linux64.tar.gz
RUN cd /usr/local/stata17 && tar -xvf /tmp/Stata17Linux64.tar.gz

RUN chown $NB_USER /usr/local/stata17/
ENV PATH=$PATH:/usr/local/stata17
RUN cd /usr/local/stata17 && \
	{ echo y; echo y; echo y; } | ./install

COPY ./resources/Stata.ipynb .
COPY ./resources/welcome.html .

USER $NB_USER
RUN pip install --user stata_setup==0.1.2

COPY ./dockerstart.sh /usr/local/bin/

RUN mkdir /tmp/custom_api
COPY ./resources/custom_api/* /tmp/custom_api/

CMD /usr/local/bin/dockerstart.sh
