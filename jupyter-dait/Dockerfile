FROM quay.io/cdis/jupyter-nde-base:1.0.2

USER root

# COPY premade notebook 
RUN mkdir /home/jovyan/DAIT-notebook

ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIT_notebook/DAIT_lipids_demo.ipynb /home/jovyan/DAIT-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIT_notebook/Microbiome.ipynb /home/jovyan/DAIT-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIT_notebook/microbiome.R /home/jovyan/DAIT-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIT_notebook/ndh_analysis_functions.py /home/jovyan/DAIT-notebook/
RUN chmod -R 777 /home/jovyan/DAIT-notebook

USER $NB_UID
WORKDIR /home/jovyan
