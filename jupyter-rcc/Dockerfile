# Base the image on official Python 3.14
FROM python:3.14-slim

USER root

# =========================================================================
# SYSTEM PACKAGES
#
# Three groups here:
#   1. Base build toolchain / utilities (unchanged).
#   2. Dev libraries needed to COMPILE CRAN packages from source. These are
#      required not because the image itself compiles them, but because users
#      install their own packages from CRAN at runtime, and CRAN only ships
#      source for Linux. Without these, common packages fail to build:
#        libuv1-dev      -> fs        (fs >= 2.x needs system libuv)
#        libgit2-dev     -> gert      (devtools dependency)
#        libicu-dev      -> stringi
#        font/image libs -> ragg, textshaping, systemfonts (ggplot2 rendering)
#        gfortran        -> minqa, lme4 and many stats packages (Fortran source)
#        libblas/lapack  -> RcppArmadillo and other linear-algebra packages
#        libpoppler-cpp-dev -> pdftools
#        libmagick++-dev    -> magick (ImageMagick bindings)
#   3. Requested R packages that Debian ships as prebuilt binaries. Using apt
#      here avoids source compilation entirely (fast, and no build failures).
#      NOTE: r-cran-devtools also pulls in binary gert/fs/usethis, which are
#      exactly the packages that fail to compile from CRAN. r-cran-survey and
#      friends are here because they are tableone's dependencies, and building
#      survey from CRAN drags in minqa/RcppArmadillo. r-cran-r.utils is needed
#      for data.table::fread() to read gzipped files (.maf.gz, .vcf.gz, etc).
#
# Packages already provided by r-cran-tidyverse (dplyr, lubridate, stringr,
# magrittr, broom) are listed anyway for documentation; apt will no-op them.
# 'coxph' is not a package -- it is a function in the 'survival' package.
# 'grid' is not listed because it is a base R package shipped with r-base-core;
# library(grid) works with no installation.
# =========================================================================
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    gfortran \
    make \
    libblas-dev \
    liblapack-dev \
    libxml2-dev \
    libssl-dev \
    libcurl4-openssl-dev \
    libssh2-1-dev \
    zlib1g-dev \
    libgsl-dev \
    ghostscript \
    unzip \
    wget \
    tar \
    gzip \
    git \
    curl \
    r-base \
    r-cran-tidyverse \
    libzmq3-dev \
    less \
    vim \
    libuv1-dev \
    libgit2-dev \
    libicu-dev \
    libfontconfig1-dev \
    libharfbuzz-dev \
    libfribidi-dev \
    libfreetype6-dev \
    libpng-dev \
    libtiff5-dev \
    libjpeg-dev \
    libpoppler-cpp-dev \
    libmagick++-dev \
    r-cran-devtools \
    r-cran-broom \
    r-cran-survival \
    r-cran-data.table \
    r-cran-dplyr \
    r-cran-lubridate \
    r-cran-magrittr \
    r-cran-mass \
    r-cran-pbapply \
    r-cran-reshape2 \
    r-cran-stringi \
    r-cran-stringr \
    r-cran-sqldf \
    r-cran-testthat \
    r-cran-rjava \
    r-cran-survey \
    r-cran-e1071 \
    r-cran-zoo \
    r-cran-gmodels \
    r-cran-nlme \
    r-cran-labelled \
    r-cran-r.utils \
    r-cran-pdftools \
    r-cran-jpeg \
    r-cran-png \
    r-cran-magick \
    && rm -rf /var/lib/apt/lists/*

# needs jupyterlab for IRkernel
RUN pip3 install jupyterlab

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
#      REQUIRED to actually keep these entries gone. (The old restricted-download
#      image predated 4.1 and did not need this step.)

RUN jupyter labextension disable @jupyterlab/docmanager-extension:download \
                                 @jupyterlab/filebrowser-extension:download \
                                 @jupyterlab/notebook-extension:export && \
    jupyter labextension lock    @jupyterlab/docmanager-extension:download \
                                 @jupyterlab/filebrowser-extension:download \
                                 @jupyterlab/notebook-extension:export

# Install IRkernel and register it for JupyterLab globally
# needs to be root user to install packages
RUN R -e "install.packages('IRkernel', repos='https://cloud.r-project.org'); if (!requireNamespace('IRkernel', quietly=TRUE)) quit(status=1, save='no')" && \
    R -e "IRkernel::installspec(user = FALSE)"

# =========================================================================
# R PACKAGES NOT PACKAGED BY DEBIAN -- installed from CRAN (compiled)
#   comorbidity, fst, tableone : no r-cran-* equivalent exists
#   xlsx                       : needs rJava (installed above via apt)
# install.packages() only warns on failure, so verify explicitly and fail
# the build if anything did not install.
# =========================================================================
RUN R -e "pkgs <- c('comorbidity','fst','tableone','xlsx'); \
          install.packages(pkgs, repos='https://cloud.r-project.org'); \
          missing <- setdiff(pkgs, rownames(installed.packages())); \
          if (length(missing)) { cat('FAILED TO INSTALL:', paste(missing, collapse=', '), '\n'); quit(status=1, save='no') }"

# For Gen3 workspaces create the jovyan group with GID 101, then create user jovyan with UID 1010 and group name jovyan
RUN groupadd -g 101 jovyan && \
    useradd -m -s /bin/bash -u 1010 -g jovyan jovyan

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
#     starts and lands FIRST in .libPaths(). This matters: setting
#     .libPaths() from inside a notebook is too late, since IRkernel has
#     already loaded rlang/cli/vctrs from site-library by then, which causes
#     "namespace 'rlang' is already loaded, but >= x.y.z is required" errors.
#
# The directory itself is created in start-notebook.sh, not here: pd is a
# runtime mount (anything created at build time is masked), and R silently
# ignores R_LIBS_USER if the directory does not exist.
# =========================================================================
ENV R_LIBS_USER="/home/jovyan/pd/r_libraries"

# =========================================================================
# IMPORT AND AUTHORIZE THE STARTUP WRAPPER SCRIPT
# Copy the script into a global system directory path and make it executable
# =========================================================================
COPY start-notebook.sh /usr/local/bin/start-notebook.sh
RUN chmod +x /usr/local/bin/start-notebook.sh

# Switch to the secure Gen3 user context permanently for all subsequent build steps
USER jovyan

# Copy requirements and compile packages
COPY requirements.txt .
RUN pip3 install --user --no-cache-dir --upgrade pip setuptools wheel && \
    pip3 install --user --no-cache-dir -r requirements.txt

# Pre-download genomes directly into the safe internal home directory path
ENV SIGPROFILERMATRIXGENERATOR_VOLUME="/home/jovyan/reference_genomes"
RUN SigProfilerMatrixGenerator install GRCh38 && \
    SigProfilerMatrixGenerator install GRCh37

# Force JupyterLab terminal interface to spawn full Bash shell sessions instead of basic /bin/sh
ENV SHELL="/bin/bash"

# Expose standard Jupyter runtime port for Gen3 proxy routing
EXPOSE 8888

# Start notebook using standard entrypoint form to properly inherit Gen3 command/args array
ENTRYPOINT ["start-notebook.sh"]
