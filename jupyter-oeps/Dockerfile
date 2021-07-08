FROM quay.io/cdis/jupyter-notebook:1.1.0

RUN git clone https://github.com/mbkranz/oeps-r-library.git
RUN sh oeps-r-library/install_conda_packages.sh

USER $NB_USER
WORKDIR /home/$NB_USER

COPY ./resources/requirements.txt ${HOME}/

COPY ./resources/oeps-toolkit-heal-platform-demo.ipynb ${HOME}/

RUN pip install -r ${HOME}/requirements.txt
