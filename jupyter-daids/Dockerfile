FROM quay.io/cdis/jupyter-nde-base:1.0.2

USER root

# COPY premade notebook
RUN mkdir /home/jovyan/daids-notebook
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIDS_notebook/nde_aids_pynb.ipynb /home/jovyan/daids-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIDS_notebook/nde_aids_function.py /home/jovyan/daids-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/DAIDS_notebook/readme.txt /home/jovyan/daids-notebook/
RUN chmod -R 777 /home/jovyan/daids-notebook
RUN touch /home/jovyan/daids-notebook/readme.txt
RUN touch /home/jovyan/daids-notebook/de_aids_pynb.ipynb
RUN touch /home/jovyan/daids-notebook/nde_aids_function.py

USER $NB_UID
WORKDIR /home/jovyan
