FROM quay.io/cdis/jupyter-nde-base:1.0.2

USER root

# COPY premade notebook 
RUN mkdir /home/jovyan/DAIT-notebook

ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIT_notebook/DAIT_lipids_demo.ipynb /home/jovyan/DAIT-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIT_notebook/Microbiome.ipynb /home/jovyan/DAIT-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIT_notebook/microbiome.R /home/jovyan/DAIT-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIT_notebook/ndh_analysis_functions.py /home/jovyan/DAIT-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIT_notebook/readme.txt /home/jovyan/DAIT-notebook/
RUN chmod -R 777 /home/jovyan/DAIT-notebook
RUN touch /home/jovyan/DAIT-notebook/DAIT_lipids_demo.ipynb
RUN touch /home/jovyan/DAIT-notebook/Microbiome.ipynb
RUN touch /home/jovyan/DAIT-notebook/microbiome.R
RUN touch /home/jovyan/DAIT-notebook/ndh_analysis_functions.py
RUN touch /home/jovyan/DAIT-notebook/readme.txt

USER $NB_UID
WORKDIR /home/jovyan
