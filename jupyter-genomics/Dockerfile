# Base the image on jupyterlab-generic
FROM quay.io/cdis/jupyterlab-generic:master

USER root

# =========================================================================
# SYSTEM PACKAGES
#
# This is a SLIM image for testing software-library requirements. It ships
# only general-purpose compilers and system libraries, so that users can
# install their own R and Python packages at runtime without hitting a
# "system library not found" build wall. It intentionally does NOT preinstall
# any domain-specific R packages, Python science stack, SigProfiler, or
# reference genomes -- those are left for the user to install and test.
#
# The dev libraries below are general (not tied to any one bioinformatics
# package). They cover the common compile-time dependencies of CRAN packages:
#   libzmq3-dev        -> IRkernel (required for the R kernel to build/run)
#   libuv1-dev         -> fs (devtools dependency chain)
#   libgit2-dev        -> gert (devtools dependency chain)
#   libicu-dev         -> stringi (text handling; very common)
#   font / image libs  -> ragg, textshaping, systemfonts (ggplot2 rendering)
#   gfortran           -> minqa, lme4 and many stats packages (Fortran source)
#   libblas/lapack     -> RcppArmadillo and other linear-algebra packages
#   libpoppler-cpp-dev -> pdftools
#   libmagick++-dev    -> magick (ImageMagick bindings)
# =========================================================================
RUN dnf install -y \
    gcc \
    gcc-c++ \
    gcc-gfortran \
    make \
    blas-devel \
    lapack-devel \
    libxml2-devel \
    openssl-devel \
    libcurl-devel \
    libssh2-devel \
    zlib-devel \
    gsl-devel \
    ghostscript \
    unzip \
    wget \
    tar \
    gzip \
    git \
    R-core-devel \
    zeromq-devel \
    less \
    vim-enhanced \
    libuv-devel \
    libgit2-devel \
    libicu-devel \
    fontconfig-devel \
    harfbuzz-devel \
    fribidi-devel \
    freetype-devel \
    libpng-devel \
    libtiff-devel \
    libjpeg-turbo-devel \
    poppler-cpp-devel \
    ImageMagick-c++-devel \
    && dnf clean all

# Install classic notebook frontend.
# notebook pulls in nbclient and the rest of the runtime, so it is not listed
# separately.
# JupyterLab + a Python kernel (ipykernel) already installed in base image
RUN pip3 install notebook

# RESTRICT DOWNLOADS / EXPORT (so no data leaves the workspace)
#   1. Disable the plugins that let users pull data out of the workspace:
#        - filebrowser-extension:download -> "Download" in the file browser
#          right-click context menu
#        - docmanager-extension:download  -> "Download" in the File menu for
#          the currently open document
#        - notebook-extension:export      -> "Save and Export Notebook As..."
#          (PDF / HTML / etc.) in the notebook File menu
#   2. LOCK them. On JupyterLab >= 4.1 a merely-disabled plugin can be
#      re-enabled by the user via Settings / Extension Manager, so locking is
#      REQUIRED to actually keep these entries gone.
RUN jupyter labextension disable @jupyterlab/docmanager-extension:download \
                                 @jupyterlab/filebrowser-extension:download \
                                 @jupyterlab/notebook-extension:export && \
    jupyter labextension lock    @jupyterlab/docmanager-extension:download \
                                 @jupyterlab/filebrowser-extension:download \
                                 @jupyterlab/notebook-extension:export

# Install IRkernel and register it for JupyterLab globally.
# needs to be root user to install packages
RUN R -e "install.packages('IRkernel', repos='https://cloud.r-project.org'); if (!requireNamespace('IRkernel', quietly=TRUE)) quit(status=1, save='no')" && \
    R -e "IRkernel::installspec(user = FALSE)"


ENV HOME=/home/jovyan
WORKDIR $HOME

# Setup default placeholder directories and fix base permissions
RUN mkdir -p /home/jovyan/pd && chown -R jovyan:jovyan /home/jovyan

# Add user binary paths to environment PATH so CLI commands execute globally
ENV PATH="/home/jovyan/.local/bin:${PATH}"

# =========================================================================
# R USER LIBRARY ON THE PERSISTENT DRIVE
#
# Lets users run install.packages('foo') / library('foo') with no setup:
#   - /usr/local/lib/R/site-library is root-owned and NOT writable by jovyan,
#     so without this R errors out ("lib is not writable") in the IRkernel.
#   - /home/jovyan/pd is the only persistent path, so packages survive restarts.
#   - Because R_LIBS_USER is an env var, it is applied when the R process
#     starts and lands FIRST in .libPaths().
#
# The directory itself is created in start-notebook.sh, not here: pd is a
# runtime mount (anything created at build time is masked), and R silently
# ignores R_LIBS_USER if the directory does not exist.
# =========================================================================
ENV R_LIBS_USER="/home/jovyan/pd/r_libraries"

# =========================================================================
# PYTHON USER PACKAGES ON THE PERSISTENT DRIVE
#
# Mirrors R_LIBS_USER for Python. PYTHONUSERBASE controls BOTH where
# `pip install --user` writes AND where `import` looks, so pointing it at pd
# makes user-installed packages persist across restarts with no setup:
#   pip install --user <pkg>  ->  /home/jovyan/pd/py_libraries/lib/.../site-packages
#   import <pkg>              ->  loaded from there
#
# There is no build-time `pip install --user` in this slim image, so there is
# no risk of build-time packages landing under pd. The directory is created in
# start-notebook.sh since pd only exists at runtime.
# =========================================================================
ENV PYTHONUSERBASE="/home/jovyan/pd/py_libraries"
ENV PATH="/home/jovyan/pd/py_libraries/bin:${PATH}"

# =========================================================================
# IMPORT AND AUTHORIZE THE STARTUP WRAPPER SCRIPT
# Copy the script into a global system directory path and make it executable
# =========================================================================
COPY start-notebook.sh /usr/local/bin/start-notebook.sh
RUN chmod +x /usr/local/bin/start-notebook.sh

# Switch to the secure Gen3 user context permanently for all subsequent build steps
USER jovyan

# NOTE: no build-time `pip install --user` here. PYTHONUSERBASE points at pd,
# which is a runtime mount, so anything installed --user at build time would be
# masked and lost when pd mounts. Users install packages at runtime, where they
# persist under pd via PYTHONUSERBASE.

# Force JupyterLab terminal interface to spawn full Bash shell sessions instead of basic /bin/sh
ENV SHELL="/bin/bash"

# Expose standard Jupyter runtime port for Gen3 proxy routing
EXPOSE 8888

# Start notebook using standard entrypoint form to properly inherit Gen3 command/args array
ENTRYPOINT ["start-notebook.sh"]

# Clear the inherited CMD from the base image and use the Entrypoint defined above by default
CMD []
