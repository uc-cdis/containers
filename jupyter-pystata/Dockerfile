FROM quay.io/cdis/jupyter-notebook:1.1.0

USER root
RUN apt-get update

# needed if user wants to run stinit (license validation) in the workspace
RUN	apt-get install -y libncurses5

RUN mkdir /usr/local/stata17
COPY jupyter-pystata/resources/Stata17Linux64.tar.gz /tmp/Stata17Linux64.tar.gz
RUN cd /usr/local/stata17 && tar -xvf /tmp/Stata17Linux64.tar.gz

RUN chown $NB_USER /usr/local/stata17/
ENV PATH $PATH:/usr/local/stata17
RUN cd /usr/local/stata17 && \
	{ echo y; echo y; echo y; } | ./install

COPY jupyter-pystata/resources/Stata.ipynb $NB_WORKDIR

# Allow notebook to run withing an <iframe/>
RUN echo "c.NotebookApp.tornado_settings = {\"headers\": {\"Content-Security-Policy\": \"frame-ancestors 'self'\"}}" \
	>> /home/$NB_USER/.jupyter/jupyter_notebook_config.py

# When an iPython session starts, check the ~/pd/ directory for a stata.lic license file and copy if present
RUN mkdir -p /home/$NB_USER/.ipython \
			 /home/$NB_USER/.ipython/profile_default/ \
			 /home/$NB_USER/.ipython/profile_default/startup/
COPY jupyter-pystata/resources/copy_license_on_startup.py \
	/home/$NB_USER/.ipython/profile_default/startup/copy_license_on_startup.py

USER $NB_USER
RUN pip install --user stata_setup

# COPY jupyter-pystata/resources/wait_for_license.sh /tmp/wait_for_license.sh
