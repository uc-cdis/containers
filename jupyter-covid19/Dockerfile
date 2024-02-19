FROM quay.io/cdis/jupyter-notebook:restricted-download-1.3.1

USER $NB_USER
WORKDIR /home/$NB_USER
ARG COVID_TOOLS_BRANCH=master

# copy welcome splash page
ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/welcome.html /home/$NB_USER/
RUN touch /home/$NB_USER/welcome.html

# copy readme and notebooks requirements
RUN mkdir /home/$NB_USER/covid19-notebook

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/readme.md /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/readme.md

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/requirements.txt /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/requirements.txt

# copy premade notebooks
ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/jhu-summary-overview/COVID-19-JHU_data_analysis.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/COVID-19-JHU_data_analysis.ipynb

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/kaggle-demographics/kaggle_data_analysis.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/kaggle_data_analysis.ipynb

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/chicago-seir-forecast/covid19_seir.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/covid19_seir.ipynb

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/chicago-seir-forecast/seir_diagram.png /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/seir_diagram.png

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/ctp_testing/CTP_testing.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/CTP_testing.ipynb

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/TCGA_COAD_COVID.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/TCGA_COAD_COVID.ipynb

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/nCoV-2019_data_analysis.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/nCoV-2019_data_analysis.ipynb

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/SSR/SSR_notebook.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/SSR_notebook.ipynb

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/X-ray/DarkCovidNet_binary_classes.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/DarkCovidNet_binary_classes.ipynb

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/X-ray/CNN_XRAY_CF.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/CNN_XRAY_CF.ipynb

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/google_mobility.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/google_mobility.ipynb

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/pypfb/PFB_example.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/PFB_example.ipynb

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/IL_tab_charts.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/IL_tab_charts.ipynb

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/3D_Protein_Vis/3D_Protein_Vis.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/3D_Protein_Vis.ipynb

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/3D_Protein_Vis/3D_Protein_Vis_7D4F_gui.png /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/3D_Protein_Vis_7D4F_gui.png

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/3D_Protein_Vis/3D_Protein_Vis_7D4F_view.html /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/3D_Protein_Vis_7D4F_view.html

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/3D_Protein_Vis/3D_Protein_Vis_A_view.html /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/3D_Protein_Vis_A_view.html

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/3D_Protein_Vis/3D_Protein_Vis_B_view.html /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/3D_Protein_Vis_B_view.html

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/3D_Protein_Vis/3D_Protein_Vis_demo_view.html /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/3D_Protein_Vis_demo_view.html

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/ICU_prediction/Percentage_ICU_prediction.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/Percentage_ICU_prediction.ipynb

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/extended-seir/extended-seir.ipynb /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/extended-seir.ipynb

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/extended-seir/extended-seir_diagram.png /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/extended-seir_diagram.png

ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/extended-seir/extended-seir_parameters.png /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/extended-seir_parameters.png

# small pfb file
ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/pypfb/PFB_example.avro /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/PFB_example.avro

# peregrine helper script required by the X-ray notebooks
ADD --chown=$NB_USER:users https://raw.githubusercontent.com/uc-cdis/covid19-tools/$COVID_TOOLS_BRANCH/covid19-notebooks/X-ray/peregrine.py /home/$NB_USER/covid19-notebook/
RUN touch /home/$NB_USER/covid19-notebook/peregrine.py

# premade notebooks dependencies
RUN pip install -U -r /home/$NB_USER/covid19-notebook/requirements.txt

# The image can't function (see error below) with `jsonschema` version 3.2.0. Some dependencies are
# preventing `jsonschema` from being upgraded to a more recent version. Updating it here as a quick fix.
#   File "/usr/local/lib/python3.9/dist-packages/jupyter_events/validators.py", line 44, in <module>
#     JUPYTER_EVENTS_SCHEMA_VALIDATOR = Draft7Validator(
# TypeError: __init__() got an unexpected keyword argument 'registry'
RUN pip install jsonschema==4.20.0 --upgrade
