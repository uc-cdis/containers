FROM quay.io/cdis/jupyter-nde-base:chore_nde_base

USER root

# COPY premade notebook 
RUN mkdir /home/jovyan/DMID-notebook

ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DMID_notebook/CalU3_TypeI_ISG.txt /home/jovyan/DMID-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DMID_notebook/DMID-LHV-R.ipynb /home/jovyan/DMID-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DMID_notebook/LHV_demo.ipynb /home/jovyan/DMID-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DMID_notebook/ndh_analysis_function_dmid.r /home/jovyan/DMID-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DMID_notebook/ndh_analysis_functions_dmid.py /home/jovyan/DMID-notebook/
RUN chmod -R 777 /home/jovyan/tb-notebook

USER $NB_UID
WORKDIR /home/jovyan
