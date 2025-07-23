FROM quay.io/cdis/jupyter-superslim:fix_al2

USER root

RUN mkdir /usr/local/stata18
COPY ./resources/StataNow18Linux64.tar.gz /tmp/StataNow18Linux64.tar.gz
RUN cd /usr/local/stata18 && tar -xvf /tmp/StataNow18Linux64.tar.gz

ENV PATH=$PATH:/usr/local/stata18
RUN cd /usr/local/stata18 && \
	{ echo y; echo y; echo y; } | ./install

COPY ./resources/Stata.ipynb .
COPY ./resources/welcome.html .

RUN chown -R $NB_USER /usr/local/stata18/
USER $NB_USER
RUN pip install --user stata_setup

COPY ./dockerstart.sh /usr/local/bin/

RUN mkdir /tmp/custom_api
COPY ./resources/custom_api/* /tmp/custom_api/

CMD /usr/local/bin/dockerstart.sh
