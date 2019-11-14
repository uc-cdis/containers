FROM quay.io/cdis/jupyter-nde-base:1.0.2

USER root

# COPY premade notebook 
RUN mkdir /home/jovyan/daids-notebook

ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIDS_notebook/CHARLIE_demo.ipynb /home/jovyan/daids-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIDS_notebook/ndh_analysis_functions.py /home/jovyan/daids-notebook/
RUN chmod -R 777 /home/jovyan/daids-notebook

USER $NB_UID
WORKDIR /home/jovyan
