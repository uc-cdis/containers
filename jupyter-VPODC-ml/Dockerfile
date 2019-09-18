FROM tf_docker/py3tensor:v1
RUN apt-get install -y openslide-tools && apt-get install -y python-openslide  

RUN pip install openslide-python && pip install dicom && pip install oauthlib

RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -

RUN apt-get update && \
    apt-get install -y git bzip2 nodejs libssl-dev && \
    apt-get clean && \
    rm -rf /var/tmp /tmp /var/lib/apt/lists/*

RUN curl -sSL -o installer.sh https://repo.continuum.io/archive/Anaconda3-4.2.0-Linux-x86_64.sh && \
    bash /installer.sh -b -f && \
    rm /installer.sh


RUN npm install -g configurable-http-proxy && \
    pip install --no-cache-dir \
                 notebook \
                 jupyterhub-kubespawner==0.9.* \
                 git+https://github.com/jupyterhub/jupyterhub.git@dcdb8d8a89d98cda411f00ac92b99f008ffaefd6 \
                 git+https://github.com/occ-data/jhub_remote_user_authenticator.git@53d22afbc5f75441169974fd98580d967600d700 \
                 pycurl==7.43.0.3 \
                 oauthlib

ADD model.ckpt-112000.data-00000-of-00001 /
ADD model.ckpt-112000.index /
ADD model.ckpt-112000.meta /
ADD cull_idle_servers.py /usr/local/bin/cull_idle_servers.py

ENTRYPOINT jupyterhub
