ARG ROOT_CONTAINER=quay.io/cdis/amazonlinux:latest

ARG BASE_CONTAINER=$ROOT_CONTAINER
FROM $BASE_CONTAINER

ARG NB_USER="jovyan"
ARG NB_UID="1000"
ARG NB_GID="100"

# Fix DL4006
SHELL ["/bin/bash", "-o", "pipefail", "-c"]

USER root

# Install all OS dependencies for notebook server that starts but lacks all
# features (e.g., download as all possible file formats)
ENV DEBIAN_FRONTEND noninteractive
RUN dnf upgrade &&\
    dnf install -yq \
    bzip2 \
    ca-certificates \
    glibc-locale-source \
    sudo \
    # tini \ cannot install tini from dnf, but installed it later using mamba
    wget \
    # tar is not available by default in al2023 [Amazon linux 2023]
    tar \
    # shadow-utils is needed to run the `useradd` command
    shadow-utils \
    # findutils is needed to run the `find` command
    findutils \
    # - pandoc is used to convert notebooks to html files
    #CTDS NOTES:
    #   It is not available in AL2023 (https://github.com/amazonlinux/amazon-linux-2023/issues/379)
    #   Need to find an alternative maybe.
    # pandoc \
    # - run-one - a wrapper script that runs no more
    #   than one unique  instance  of  some  command with a unique set of arguments,
    #   we use `run-one-constantly` to support `RESTARTABLE` option
    #CTDS NOTES:  Couild not find an alternative in Amazon Linux for this package.
    # run-one \
    && dnf clean all

RUN localedef -i en_US -f UTF-8 en_US.UTF-8

# Configure environment
ENV CONDA_DIR=/opt/conda \
    SHELL=/bin/bash \
    NB_USER="${NB_USER}" \
    NB_UID=${NB_UID} \
    NB_GID=${NB_GID} \
    LC_ALL=en_US.UTF-8 \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8
ENV PATH="${CONDA_DIR}/bin:${PATH}" \
    HOME="/home/${NB_USER}"

RUN mkdir /opt/downloads
# Copy a script that we will use to correct permissions after running certain commands
COPY resource_file_urls.txt /opt/downloads
RUN cd /opt/downloads && \
    wget -i resource_file_urls.txt && \
    mv fix-permissions /usr/local/bin/fix-permissions && \
    chmod a+rx /usr/local/bin/fix-permissions && cd /

# Enable prompt color in the skeleton .bashrc before creating the default NB_USER
# hadolint ignore=SC2016
RUN sed -i 's/^#force_color_prompt=yes/force_color_prompt=yes/' /etc/skel/.bashrc && \
   # Add call to conda init script see https://stackoverflow.com/a/58081608/4413446
   echo 'eval "$(command conda shell.bash hook 2> /dev/null)"' >> /etc/skel/.bashrc


# Create NB_USER with name jovyan user with UID=1000 and in the 'users' group
# and make sure these dirs are writable by the `users` group.
RUN echo "auth requisite pam_deny.so" >> /etc/pam.d/su && \
    sed -i.bak -e 's/^%admin/#%admin/' /etc/sudoers && \
    sed -i.bak -e 's/^%sudo/#%sudo/' /etc/sudoers && \
    useradd --no-log-init --create-home --shell /bin/bash --uid "${NB_UID}" --no-user-group "${NB_USER}" && \
    mkdir -p "${CONDA_DIR}" && \
    chown "${NB_USER}:${NB_GID}" "${CONDA_DIR}" && \
    chmod g+w /etc/passwd && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}" && \
    mv /opt/downloads/initial-condarc ${CONDA_DIR}/.condarc && \
    chown ${NB_UID}:${NB_GID} ${CONDA_DIR}/.condarc

USER ${NB_UID}

ARG PYTHON_VERSION=default

# Setup work directory for backward-compatibility
RUN mkdir "/home/${NB_USER}/work" && \
    fix-permissions "/home/${NB_USER}"

# Download and install Micromamba, and initialize Conda prefix.
#   <https://github.com/mamba-org/mamba#micromamba>
#   Similar projects using Micromamba:
#     - Micromamba-Docker: <https://github.com/mamba-org/micromamba-docker>
#     - repo2docker: <https://github.com/jupyterhub/repo2docker>
# Install Python, Mamba and jupyter_core
# Cleanup temporary files and remove Micromamba
# Correct permissions
# Do all this in a single RUN command to avoid duplicating all of the
# files across image layers when the permissions change



WORKDIR /tmp

RUN set -x && \
    arch=$(uname -m) && \
    if [ "${arch}" = "x86_64" ]; then \
        # Should be simpler, see <https://github.com/mamba-org/mamba/issues/1437>
        arch="64"; \
    fi && \
    wget --progress=dot:giga -O /tmp/micromamba.tar.bz2 \
        "https://micromamba.snakepit.net/api/micromamba/linux-${arch}/latest" && \
    tar -xvjf /tmp/micromamba.tar.bz2 --strip-components=1 bin/micromamba && \
    rm /tmp/micromamba.tar.bz2 && \
    PYTHON_SPECIFIER="python=${PYTHON_VERSION}" && \
    if [[ "${PYTHON_VERSION}" == "default" ]]; then PYTHON_SPECIFIER="python"; fi && \
    # Install the packages
    ./micromamba install \
        --root-prefix="${CONDA_DIR}" \
        --prefix="${CONDA_DIR}" \
        --yes \
        "${PYTHON_SPECIFIER}" \
        'mamba' \
        'jupyter_core' && \
    rm micromamba && \
    # Pin major.minor version of python
    mamba list python | grep '^python ' | tr -s ' ' | cut -d ' ' -f 1,2 >> "${CONDA_DIR}/conda-meta/pinned" && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"



# Install Tini
RUN mamba install --quiet --yes 'tini=0.18.0' && \
    mamba list tini | grep tini | tr -s ' ' | cut -d ' ' -f 1,2 >> $CONDA_DIR/conda-meta/pinned && \
    conda clean --all -f -y && \
    fix-permissions $CONDA_DIR && \
    fix-permissions /home/$NB_USER

# # Configure container startup
ENTRYPOINT ["tini", "-g", "--"]

USER root

RUN mv /opt/downloads/run-hooks.sh /opt/downloads/start.sh /usr/local/bin/

# Create dirs for startup hooks
RUN mkdir /usr/local/bin/start-notebook.d && \
    mkdir /usr/local/bin/before-notebook.d

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

WORKDIR "${HOME}"


# Install JupyterLab, Jupyter Notebook, JupyterHub and NBClassic
# Generate a Jupyter Server config
# Cleanup temporary files
# Correct permissions
# Do all this in a single RUN command to avoid duplicating all of the
# files across image layers when the permissions change
WORKDIR /tmp
RUN mamba install --yes \
    'jupyterlab' \
    'notebook' \
    'jupyterhub' \
    'nbclassic' && \
    jupyter server --generate-config && \
    mamba clean --all -f -y && \
    npm cache clean --force && \
    jupyter lab clean && \
    rm -rf "/home/${NB_USER}/.cache/yarn" && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

ENV JUPYTER_PORT=8888
EXPOSE $JUPYTER_PORT

# Fix permissions on /etc/jupyter as root
USER root

# Configure container startup
CMD ["start-notebook.sh"]


RUN mv /opt/downloads/start-notebook.sh /opt/downloads/start-singleuser.sh /usr/local/bin/ && \
chmod a+rx /usr/local/bin/* && \
mkdir -p /etc/jupyter && \
mv /opt/downloads/jupyter_server_config.py /opt/downloads/docker_healthcheck.py /etc/jupyter/ && \
fix-permissions /etc/jupyter/

# HEALTHCHECK documentation: https://docs.docker.com/engine/reference/builder/#healthcheck
# This healtcheck works well for `lab`, `notebook`, `nbclassic`, `server` and `retro` jupyter commands
# https://github.com/jupyter/docker-stacks/issues/915#issuecomment-1068528799
HEALTHCHECK --interval=5s --timeout=3s --start-period=5s --retries=3 \
    CMD /etc/jupyter/docker_healthcheck.py || exit 1

# Switch back to jovyan to avoid accidental container runs as root
USER ${NB_UID}

WORKDIR "${HOME}"


# # ############################## Dockerfile for azlinux-minimal ########################
USER root

RUN dnf install -yq \
    libcurl-minimal \
    curl-minimal \
    git \
    tzdata \
    unzip \
    openssh-clients \
    nano \
    vim-minimal \
    # less is needed to run help in R
    # see: https://github.com/jupyter/docker-stacks/issues/1588
    # nbconvert dependencies
    less \
    # https://nbconvert.readthedocs.io/en/latest/install.html#installing-tex
    texlive-xetex \
    texlive-collection-fontsrecommended \
    texlive-collection-plaingeneric \
    # Enable clipboard on Linux host systems
    # CTDS notes: cannot install xclip since it is a part of
    # Epel repositories which arent' a part of Amazon linux 2023 (https://linux.how2shout.com/can-we-install-epel-repo-on-amazon-linux-2023/#:~:text=RHEL%2Dbased%20systems.-,Can%20we%20install%20EPEL%20on%20Amazon%20Linux%202023%3F,NO)
    #xclip \
    && dnf clean all


#     # Switch back to jovyan to avoid accidental container runs as root
    USER $NB_UID



# ############################## Dockerfile for azlinux-scipy ########################
# ARG BASE_CONTAINER=jupyter/minimal-notebook
# FROM $BASE_CONTAINER

    USER root

    # ffmpeg
    RUN dnf groupinstall -yq "Development Tools" && \
        dnf install -yq \
        texlive-cm-super \
        texlive-dvipng
        #ffmpeg &&  This is unavailable and needs to be built from static files (https://www.johnvansickle.com/ffmpeg/faq/)

    USER ${NB_UID}

    # mamba downgrades these packages to previous major versions, which causes issues
    RUN echo 'jupyterlab >=4.0.4' >> "${CONDA_DIR}/conda-meta/pinned" && \
        echo 'notebook >=7.0.2' >> "${CONDA_DIR}/conda-meta/pinned"


# Install Python 3 packages
RUN mamba install --yes \
    'altair' \
    'beautifulsoup4' \
    'bokeh' \
    'bottleneck' \
    'cloudpickle' \
    'conda-forge::blas=*=openblas' \
    'cython' \
    'dask' \
    'dill' \
    'h5py' \
    'ipympl'\
    'ipywidgets' \
    'jupyterlab-git' \
    'matplotlib-base' \
    'numba' \
    'numexpr' \
    'openpyxl' \
    'pandas' \
    'patsy' \
    'protobuf' \
    'pytables' \
    'scikit-image' \
    'scikit-learn' \
    'scipy' \
    'seaborn' \
    'sqlalchemy' \
    'statsmodels' \
    'sympy' \
    'widgetsnbextension'\
    'xlrd' && \
    mamba clean --all -f -y && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"


# Install facets which does not have a pip or conda package at the moment
WORKDIR /tmp
RUN git clone https://github.com/PAIR-code/facets && \
    jupyter nbclassic-extension install facets/facets-dist/ --sys-prefix && \
    rm -rf /tmp/facets && \
    fix-permissions "${CONDA_DIR}" && \
    fix-permissions "/home/${NB_USER}"

# Import matplotlib the first time to build the font cache.
ENV XDG_CACHE_HOME="/home/${NB_USER}/.cache/"

RUN MPLBACKEND=Agg python -c "import matplotlib.pyplot" && \
    fix-permissions "/home/${NB_USER}"

USER ${NB_UID}

WORKDIR "${HOME}"
