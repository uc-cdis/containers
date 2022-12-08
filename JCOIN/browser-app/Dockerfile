# Ubuntu 20.04 (focal)
# https://hub.docker.com/_/ubuntu/?tab=tags&name=focal
ARG ROOT_CONTAINER=quay.io/cdis/ubuntu:focal

FROM $ROOT_CONTAINER

LABEL maintainer="Phil Schumm <pschumm@uchicago.edu>"
ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

ARG STREAMLIT_SERVER_PORT=8888

RUN apt update
RUN apt install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa
RUN apt install -y python3.9 python3.9-distutils curl
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3.9 get-pip.py
COPY requirements.txt requirements.txt
RUN pip3.9 install -r requirements.txt
# watchdog fails on M1 (https://giters.com/gorakhargosh/watchdog/issues/838)
RUN pip3.9 uninstall -y watchdog
RUN apt install -y gnupg

# Fix DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Copy a script that we will use to correct permissions after running certain commands
COPY resources/scripts/fix-permissions /usr/local/bin/fix-permissions
RUN chmod a+rx /usr/local/bin/fix-permissions

# Configure environment
ENV NB_USER="${NB_USER}" \
    NB_UID=${NB_UID} \
    NB_GID=${NB_GID}

ENV HOME="/home/${NB_USER}"

# Create NB_USER in the "users" group and make sure home directory is writable
RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su && \
    useradd -l -m -s /bin/bash -N -u "${NB_UID}" "${NB_USER}" && \
    chmod g+w /etc/passwd && \
    mkdir "${HOME}/.gen3" && \
    mkdir "${HOME}/.streamlit" && \
    fix-permissions "${HOME}"

USER ${NB_UID}
WORKDIR "${HOME}"

COPY app.py app.py
COPY secrets.toml .streamlit/secrets.toml
# For local testing
# COPY credentials.json .gen3/credentials.json

EXPOSE $STREAMLIT_SERVER_PORT
ENV STREAMLIT_SERVER_PORT $STREAMLIT_SERVER_PORT
ENTRYPOINT [ "streamlit" ]
CMD ["run", "app.py"]
