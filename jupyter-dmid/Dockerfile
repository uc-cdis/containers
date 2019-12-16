FROM quay.io/cdis/jupyter-nde-base:1.0.2

USER root

# COPY premade notebook
RUN mkdir /home/jovyan/DMID-notebook

ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DMID_notebook/CalU3_TypeI_ISG.txt /home/jovyan/DMID-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DMID_notebook/nde_dmid_rnb.ipynb /home/jovyan/DMID-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DMID_notebook/nde_dmid_pynb.ipynb /home/jovyan/DMID-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DMID_notebook/nde_dmid_function.r /home/jovyan/DMID-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DMID_notebook/nde_dmid_function.py /home/jovyan/DMID-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DMID_notebook/readme.txt /home/jovyan/DMID-notebook/
RUN chmod -R 777 /home/jovyan/DMID-notebook
RUN touch /home/jovyan/DMID-notebook/CalU3_TypeI_ISG.txt
RUN touch /home/jovyan/DMID-notebook/nde_dmid_rnb.ipynb
RUN touch /home/jovyan/DMID-notebook/nde_dmid_pynb.ipynb
RUN touch /home/jovyan/DMID-notebook/nde_dmid_function.r
RUN touch /home/jovyan/DMID-notebook/nde_dmid_function.py
RUN touch /home/jovyan/DMID-notebook/readme.txt

USER $NB_UID
WORKDIR /home/jovyan
