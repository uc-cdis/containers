FROM quay.io/cdis/jupyter-notebook:1.1.0

USER $NB_USER
WORKDIR /home/$NB_USER
ARG COVID_TOOLS_BRANCH=master

# copy welcome splash page
ADD --chown=jovyan:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/welcome.html /home/$NB_USER/
RUN touch /home/$NB_USER/welcome.html

# copy readme and notebooks requirements
RUN mkdir /home/$NB_USER/covid19-notebook

ADD --chown=jovyan:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/readme.md /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/readme.md

ADD --chown=jovyan:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/requirements.txt /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/requirements.txt

# copy premade notebooks
ADD --chown=jovyan:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/jhu-summary-overview/COVID-19-JHU_data_analysis.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/COVID-19-JHU_data_analysis.ipynb

ADD --chown=jovyan:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/kaggle-demographics/kaggle_data_analysis.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/kaggle_data_analysis.ipynb

ADD --chown=jovyan:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/chicago-seir-forecast/covid19_seir.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/covid19_seir.ipynb

ADD --chown=jovyan:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/chicago-seir-forecast/seir_diagram.png /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/seir_diagram.png

ADD --chown=jovyan:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/ctp_testing/CTP_testing.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/CTP_testing.ipynb

ADD --chown=jovyan:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/TCGA_OV_COVID.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/TCGA_OV_COVID.ipynb

ADD --chown=jovyan:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/symptoms_and_fatality_covid19.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/symptoms_and_fatality_covid19.ipynb

ADD --chown=jovyan:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/SSR/SSR_notebook.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/SSR_notebook.ipynb

ADD --chown=jovyan:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/X-ray/DarkCovidNet_binary_classes.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/DarkCovidNet_binary_classes.ipynb

ADD --chown=jovyan:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/X-ray/DarkCovidNet_three_classes.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/DarkCovidNet_three_classes.ipynb

# peregrine helper script required by the X-ray notebooks
ADD --chown=jovyan:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/X-ray/peregrine.py /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/peregrine.py

# premade notebooks dependencies
RUN pip install --upgrade 'pip<20.3' # pip 20.3 causes dependency resolution issues
RUN pip install -r /home/$NB_USER/covid19-notebook/requirements.txt
