FROM quay.io/cdis/jupyter-notebook:1.0.1

USER root

RUN apt-get update && \
    apt-get install -y \
    mummer

RUN git clone https://github.com/sanger-pathogens/ariba.git \
  && cd ariba \
  && git checkout v2.13.4 \
  # && python3 setup.py test \
  && python3 setup.py install

RUN git clone https://github.com/Mykrobe-tools/mykrobe.git mykrobe \
    && cd mykrobe

WORKDIR mykrobe

## Download pre-built probesets
RUN wget -O mykrobe-data.tar.gz https://bit.ly/2H9HKTU && tar -zxvf mykrobe-data.tar.gz && rm -fr src/mykrobe/data && mv mykrobe-data src/mykrobe/data

RUN pip install .

## Append custom settings to jupyter config file
COPY jupyter_notebook_config.py /home/$NB_USER/.jupyter/tmp.py
RUN cat /home/$NB_USER/.jupyter/tmp.py >> /home/$NB_USER/.jupyter/jupyter_notebook_config.py && rm /home/$NB_USER/.jupyter/tmp.py


# COPY premade notebook 
RUN mkdir /home/jovyan/tb-notebook
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/TB_notebook/NIAID_plots_2.r /home/jovyan/tb-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/TB_notebook/prediction_tool_visualization.ipynb /home/jovyan/tb-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/TB_notebook/tb_analysis_function.py /home/jovyan/tb-notebook/
ADD https://raw.githubusercontent.com/uc-cdis/ndh-demo/master/demo/TB_notebook/tb_notebook.ipynb /home/jovyan/tb-notebook/
RUN chmod -R 777 /home/jovyan/tb-notebook

# CMD ariba

USER $NB_UID
WORKDIR /home/jovyan