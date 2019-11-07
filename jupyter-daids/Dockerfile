FROM quay.io/cdis/jupyter-nde-base:fix_niaid-test

USER $NB_UID

# COPY premade notebook 
RUN mkdir /home/jovyan/daids-notebook

ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIDS_notebook/CHARLIE_demo.ipynb /home/jovyan/daids-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIDS_notebook/ndh_analysis_functions.py /home/jovyan/daids-notebook/

WORKDIR /home/jovyan
