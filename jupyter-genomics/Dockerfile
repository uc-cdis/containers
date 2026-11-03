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

# uv / uvx, from the official image. Pinned so builds are reproducible; bump
# the tag to upgrade. Users' uv data (Pythons, tools, cache) lives on pd, see
# the UV_* variables below.
COPY --from=ghcr.io/astral-sh/uv:0.13.7 /uv /uvx /usr/local/bin/

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

# Moving PYTHONUSERBASE off ~/.local hides the base image's Jupyter install:
# jupyterlab-generic installs JupyterLab and its extensions with `pip --user`
# into ~/.local, and Jupyter locates some of those files via USER_BASE.
# - JUPYTERLAB_DIR: without it JupyterLab falls back to
#   /usr/local/share/jupyter/lab (created by `pip3 install notebook` above, but
#   with no built assets) and fails with "application assets not found".
# - JUPYTER_CONFIG_PATH: without it ~/.local/etc/jupyter is not searched, so
#   the server extensions enabled there (jupyterlab-git, jupyterlmod, terminals,
#   lsp, archive, search-replace) are silently not loaded.
ENV JUPYTERLAB_DIR="/home/jovyan/.local/share/jupyter/lab"
ENV JUPYTER_CONFIG_PATH="/home/jovyan/.local/etc/jupyter"

# =========================================================================
# TOOL CONFIG AND DATA ON THE PERSISTENT DRIVE
#
# Point user-level tool state at pd so it survives restarts. Env vars rather
# than symlinks, because the default locations mostly can't be symlinked:
#   - uv defaults to ~/.local/share/uv and ~/.local/bin, but ~/.local holds
#     the image's JupyterLab install and must stay in the image.
#   - pre-commit defaults to ~/.cache, which also holds pip's cache.
#   - `git config --global` writes ~/.gitconfig, which isn't on pd.
# GH_CONFIG_DIR matches gh's default (~/.config is symlinked to pd/.config by
# /jupyterlab-start.sh) but is set explicitly so it doesn't depend on that.
# UV_ROOT is not a uv variable, only a shorthand for the ones below.
#
# PATH order: uv tools, then pd/tools/bin, then pd/py_libraries/bin (above).
# /jupyterlab-start.sh is patched below to restore this order after
# `module load`, so pd overrides the software library.
# =========================================================================
ENV PD="/home/jovyan/pd"
ENV GH_CONFIG_DIR="${PD}/.config/gh" \
    GIT_CONFIG_GLOBAL="${PD}/.config/git/config" \
    PRE_COMMIT_HOME="${PD}/.cache/pre-commit" \
    UV_ROOT="${PD}/.uv"
ENV UV_PYTHON_INSTALL_DIR="${UV_ROOT}/python" \
    UV_CACHE_DIR="${UV_ROOT}/cache" \
    UV_TOOL_DIR="${UV_ROOT}/tools" \
    UV_TOOL_BIN_DIR="${UV_ROOT}/bin" \
    UV_PYTHON_BIN_DIR="${UV_ROOT}/bin"
ENV PATH="${UV_TOOL_BIN_DIR}:${PD}/tools/bin:${PATH}"

# =========================================================================
# IMPORT AND AUTHORIZE THE STARTUP WRAPPER SCRIPT
# Copy the script into a global system directory path and make it executable
# =========================================================================
COPY start-notebook.sh /usr/local/bin/start-notebook.sh
RUN chmod +x /usr/local/bin/start-notebook.sh

# Drop the base image's R/ado setup from /jupyterlab-start.sh.
# The base script creates empty pd/.R and pd/.ado directories
# (`test -d ./pd/.R || mkdir ./pd/.R`) and symlinks ~/R and ~/ado into pd
# (`ln -s ./pd/R .`). ado is Stata's add-on package directory, and this image
# has no use for it or for the R symlink. The grep fails the build if any of
# these lines are still there after sed (for example, because the base image
# changed how it writes them), so the removal can't silently stop working.
RUN sed -i -E \
        -e '/^[[:space:]]*test -d \.\/pd\/\.(R|ado) \|\| mkdir \.\/pd\/\.(R|ado)[[:space:]]*$/d' \
        -e '/^[[:space:]]*ln -s \.\/pd\/(R|ado) \.[[:space:]]*$/d' \
        /jupyterlab-start.sh && \
    ! grep -nE '(mkdir \./pd/\.(R|ado)|ln -s \./pd/(R|ado))( |$)' /jupyterlab-start.sh

# Let tools on pd override the software library.
# /jupyterlab-start.sh runs `module load` after the container starts, which
# prepends /apps/... to PATH and so would shadow anything in the pd bin dirs.
# Re-prepend the pd bin dirs right before it launches JupyterLab, so the
# server, its kernels and its terminals all see pd first. The grep fails the
# build if the launch line moved and the insert did not happen.
RUN sed -i \
        '/^\/home\/jovyan\/\.local\/bin\/jupyter lab/i export PATH="${UV_TOOL_BIN_DIR}:${PD}/tools/bin:${PYTHONUSERBASE}/bin:${PATH}"' \
        /jupyterlab-start.sh && \
    grep -qxF 'export PATH="${UV_TOOL_BIN_DIR}:${PD}/tools/bin:${PYTHONUSERBASE}/bin:${PATH}"' /jupyterlab-start.sh

# =========================================================================
# USER JUPYTER KERNELS ON THE PERSISTENT DRIVE
#
# `ipykernel install --user` (and similar) writes kernelspecs to
# ~/.local/share/jupyter/kernels, which is in the image and lost on restart.
# The base image also installs its own kernels there (Python 3.14, nbstata).
#   1. Move the image's kernels to the system kernel dir (where IRkernel is),
#      so they stay owned by the image and update with it. `cp -a` overwrites
#      on a name clash, keeping the old precedence (user dir used to win).
#   2. Replace the user kernel dir with a symlink into pd. It dangles at build
#      time; start-notebook.sh creates the target once pd is mounted.
# =========================================================================
RUN mkdir -p /usr/local/share/jupyter/kernels && \
    cp -a /home/jovyan/.local/share/jupyter/kernels/. /usr/local/share/jupyter/kernels/ && \
    chown -R root:root /usr/local/share/jupyter/kernels && \
    rm -rf /home/jovyan/.local/share/jupyter/kernels && \
    ln -s /home/jovyan/pd/jupyter/kernels /home/jovyan/.local/share/jupyter/kernels && \
    chown -h jovyan:jovyan /home/jovyan/.local/share/jupyter/kernels

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
