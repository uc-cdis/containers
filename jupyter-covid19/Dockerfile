FROM quay.io/cdis/jupyter-nde-base:1.0.2
USER root

# copy welcome splash page
ADD https://raw.githubusercontent.com/uc-cdis/covid19-tools/3.1.0/covid19-notebooks/welcome.html /home/jovyan/
RUN touch /home/jovyan/welcome.html

RUN chown -R jovyan:users /home/jovyan/welcome.html

# copy premade notebooks
RUN mkdir /home/jovyan/covid19-notebook
ADD https://raw.githubusercontent.com/uc-cdis/covid19-tools/master/covid19-notebooks/jhu-summary-overview/COVID-19-JHU_data_analysis_04072020.ipynb /home/jovyan/covid19-notebook/
RUN touch /home/jovyan/covid19-notebook/COVID-19-JHU_data_analysis_04072020.ipynb

ADD https://raw.githubusercontent.com/uc-cdis/covid19-tools/master/covid19-notebooks/kaggle-demographics/kaggle_data_analysis_04072020.ipynb /home/jovyan/covid19-notebook/
RUN touch /home/jovyan/covid19-notebook/kaggle_data_analysis_04072020.ipynb

ADD https://raw.githubusercontent.com/uc-cdis/covid19-tools/master/covid19-notebooks/readme.md /home/jovyan/covid19-notebook/
RUN touch /home/jovyan/covid19-notebook/readme.md

ADD https://raw.githubusercontent.com/uc-cdis/covid19-tools/master/covid19-notebooks/requirements.txt /home/jovyan/covid19-notebook/
RUN touch /home/jovyan/covid19-notebook/requirements.txt

ADD https://raw.githubusercontent.com/uc-cdis/covid19-tools/master/covid19-notebooks/chicago-seir-forecast/covid19_seir.ipynb /home/jovyan/covid19-notebook/
RUN touch /home/jovyan/covid19-notebook/covid19_seir.ipynb

ADD https://raw.githubusercontent.com/uc-cdis/covid19-tools/master/covid19-notebooks/chicago-seir-forecast/seir_diagram.png /home/jovyan/covid19-notebook/
RUN touch /home/jovyan/covid19-notebook/seir_diagram.png

ADD https://raw.githubusercontent.com/uc-cdis/covid19-tools/master/covid19-notebooks/ctp_testing/CTP_testing.ipynb /home/jovyan/covid19-notebook/
RUN touch /home/jovyan/covid19-notebook/CTP_testing.ipynb

ADD https://raw.githubusercontent.com/uc-cdis/covid19-tools/master/covid19-notebooks/ctp_testing/TCGA_OV_COVID_tested.ipynb /home/jovyan/covid19-notebook/
RUN touch /home/jovyan/covid19-notebook/TCGA_OV_COVID_tested.ipynb

ADD https://raw.githubusercontent.com/uc-cdis/covid19-tools/master/covid19-notebooks/ctp_testing/symptoms_and_fatality_covid19_tested.ipynb /home/jovyan/covid19-notebook/
RUN touch /home/jovyan/covid19-notebook/symptoms_and_fatality_covid19_tested.ipynb

RUN chown -R jovyan:users /home/jovyan/covid19-notebook

# premade notebooks dependencies
RUN pip install -r /home/jovyan/covid19-notebook/requirements.txt

USER $NB_UID
WORKDIR /home/jovyan
