FROM quay.io/cdis/jupyter-nde-base:1.0.2

USER root

# COPY premade notebook 
RUN mkdir /home/jovyan/DMID-notebook

ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DMID_notebook/CalU3_TypeI_ISG.txt /home/jovyan/DMID-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DMID_notebook/DMID-LHV-R.ipynb /home/jovyan/DMID-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DMID_notebook/LHV_demo.ipynb /home/jovyan/DMID-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DMID_notebook/ndh_analysis_function_dmid.r /home/jovyan/DMID-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DMID_notebook/ndh_analysis_functions_dmid.py /home/jovyan/DMID-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DMID_notebook/readme.txt /home/jovyan/DMID-notebook/
RUN chmod -R 777 /home/jovyan/DMID-notebook
RUN touch home/jovyan/DMID-notebook/CalU3_TypeI_ISG.txt
RUN touch home/jovyan/DMID-notebook/DMID-LHV-R.ipynb
RUN touch home/jovyan/DMID-notebook/LHV_demo.ipynb
RUN touch home/jovyan/DMID-notebook/ndh_analysis_function_dmid.r
RUN touch home/jovyan/DMID-notebook/ndh_analysis_functions_dmid.py
RUN touch home/jovyan/DMID-notebook/readme.txt

USER $NB_UID
WORKDIR /home/jovyan
