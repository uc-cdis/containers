FROM jupyter/base-notebook:latest

USER root

RUN apt-get update && \
    apt-get install -y \
    curl \
    python3 \
    python3-pip\
    python3-dev\
    python3-setuptools \
    python3-tk \
    python3-matplotlib \
    libssl-dev libcurl4-openssl-dev \
    git bzip2 nodejs\
    build-essential cd-hit curl\
    libbz2-dev liblzma-dev \
    mummer unzip wget \
    zlib1g-dev && \
    rm -rf /var/lib/apt/lists/*

RUN python -m pip install pandas

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -

WORKDIR /

RUN wget -q http://downloads.sourceforge.net/project/bowtie-bio/bowtie2/2.2.9/bowtie2-2.2.9-linux-x86_64.zip \
    && unzip bowtie2-2.2.9-linux-x86_64.zip \
    && rm bowtie2-2.2.9-linux-x86_64.zip

# Need MPLBACKEND="agg" to make matplotlib work without X11, otherwise get the error
# _tkinter.TclError: no display name and no $DISPLAY environment variable
ENV ARIBA_BOWTIE2=$PWD/bowtie2-2.2.9/bowtie2 ARIBA_CDHIT=cdhit-est MPLBACKEND="agg"

RUN cd /usr/local/bin && ln -s /usr/bin/python3 python && cd

RUN  mkdir /notebooks

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

RUN pip3 install .

# CMD ariba

WORKDIR /notebooks
CMD /bin/sh -c "/usr/local/bin/jupyter-notebook --allow-root --no-browser --ip=0.0.0.0 --notebook-dir=/notebooks"
