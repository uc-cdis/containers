FROM quay.io/cdis/jupyter-nde-base:1.0.2

USER root

# COPY premade notebook
RUN mkdir /home/jovyan/DAIT-notebook

ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIT_notebook/nde_dait_pynb.ipynb /home/jovyan/DAIT-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIT_notebook/nde_dait_rnb.ipynb /home/jovyan/DAIT-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIT_notebook/nde_dait_function.r /home/jovyan/DAIT-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIT_notebook/nde_dait_function.py /home/jovyan/DAIT-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIT_notebook/readme.txt /home/jovyan/DAIT-notebook/
RUN chmod -R 777 /home/jovyan/DAIT-notebook
RUN touch /home/jovyan/DAIT-notebook/nde_dait_pynb.ipynb
RUN touch /home/jovyan/DAIT-notebook/nde_dait_rnb.ipynb
RUN touch /home/jovyan/DAIT-notebook/nde_dait_function.r
RUN touch /home/jovyan/DAIT-notebook/nde_dait_function.py
RUN touch /home/jovyan/DAIT-notebook/readme.txt

USER $NB_UID
WORKDIR /home/jovyan
