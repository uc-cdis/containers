FROM quay.io/cdis/jupyter-superslim:2.0.0

USER root
RUN apt-get update

# needed if user wants to run stinit (license validation) in the workspace
RUN	apt-get install -y libncurses5

RUN mkdir /usr/local/stata18
COPY ./resources/StataNow18Linux64.tar.gz /tmp/StataNow18Linux64.tar.gz
RUN cd /usr/local/stata18 && tar -xvf /tmp/StataNow18Linux64.tar.gz

RUN chown -R $NB_USER /usr/local/stata18/
ENV PATH=$PATH:/usr/local/stata18
RUN cd /usr/local/stata18 && \
	{ echo y; echo y; echo y; } | ./install

COPY ./resources/Stata.ipynb .
COPY ./resources/welcome.html .

USER $NB_USER
RUN pip install --user stata_setup

COPY ./dockerstart.sh /usr/local/bin/

RUN mkdir /tmp/custom_api
COPY ./resources/custom_api/* /tmp/custom_api/

CMD /usr/local/bin/dockerstart.sh
