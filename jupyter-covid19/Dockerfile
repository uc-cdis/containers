FROM quay.io/cdis/jupyter-nde-base:1.0.2

USER root

# COPY premade notebook
RUN mkdir /home/jovyan/covid19-notebook

ADD https://raw.githubusercontent.com/uc-cdis/covid19-tools/1.2.0/covid19-notebooks/welcome.html /home/jovyan/
ADD https://raw.githubusercontent.com/uc-cdis/covid19-tools/master/covid19-notebooks/jhu-summary-overview/COVID-19-JHU_data_analysis_04072020.ipynb /home/jovyan/covid19-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/covid19-tools/master/covid19-notebooks/kaggle-demographics/kaggle_data_analysis_04072020.ipynb /home/jovyan/covid19-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/covid19-tools/master/covid19-notebooks/readme.md /home/jovyan/covid19-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/covid19-tools/master/covid19-notebooks/requirements.txt /home/jovyan/covid19-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/covid19-tools/master/covid19-notebooks/chicago-seir-forecast/covid19_seir.ipynb /home/jovyan/covid19-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/covid19-tools/master/covid19-notebooks/chicago-seir-forecast/seir_diagram.png /home/jovyan/covid19-notebook/
RUN chmod -R 777 /home/jovyan/covid19-notebook
RUN touch /home/jovyan/welcome.html
RUN touch /home/jovyan/covid19-notebook/COVID-19-JHU_data_analysis_04072020.ipynb
RUN touch /home/jovyan/covid19-notebook/kaggle_data_analysis_04072020.ipynb
RUN touch /home/jovyan/covid19-notebook/requirements.txt
RUN touch /home/jovyan/covid19-notebook/readme.md
RUN touch /home/jovyan/covid19-notebook/covid19_seir.ipynb
RUN touch /home/jovyan/covid19-notebook/seir_diagram.png
RUN pip install -r /home/jovyan/covid19-notebook/requirements.txt

USER $NB_UID
WORKDIR /home/jovyan
