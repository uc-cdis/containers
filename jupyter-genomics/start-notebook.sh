#!/bin/bash
set -e  # Exit instantly if any single setup command fails

# -------------------------------------------------------------------------
# STEP 1: RESTORE TERMINAL ENVIRONMENT & AUTOCOMPLETION
# -------------------------------------------------------------------------
if [ ! -f "/home/jovyan/.bashrc" ]; then
    cp /etc/skel/.bash* /home/jovyan/ 2>/dev/null || true
fi

# -------------------------------------------------------------------------
# STEP 2: ENSURE THE R USER LIBRARY EXISTS ON THE PERSISTENT DRIVE
# R_LIBS_USER is set in the Dockerfile, but R silently ignores it unless the
# directory already exists. /home/jovyan/pd is only mounted at runtime, so
# this cannot be done at build time. Failure here is non-fatal: a missing R
# library path is better than the whole workspace refusing to start.
# -------------------------------------------------------------------------
mkdir -p "${R_LIBS_USER:-/home/jovyan/pd/r_libraries}" 2>/dev/null \
    || echo "WARNING: could not create R library dir ${R_LIBS_USER}"

# -------------------------------------------------------------------------
# STEP 2b: ENSURE THE PYTHON USER BASE EXISTS ON THE PERSISTENT DRIVE
# PYTHONUSERBASE is set in the Dockerfile so that `pip install --user` writes
# to pd and `import` reads from it. Like R_LIBS_USER, pd is only mounted at
# runtime, so the directory must be created here. Non-fatal on failure.
# -------------------------------------------------------------------------
mkdir -p "${PYTHONUSERBASE:-/home/jovyan/pd/py_libraries}" 2>/dev/null \
    || echo "WARNING: could not create Python user base ${PYTHONUSERBASE}"

# -------------------------------------------------------------------------
# STEP 2c: ENSURE OTHER PERSISTENT DIRECTORIES EXIST
#   - jupyter/kernels: ~/.local/share/jupyter/kernels is a symlink to it
#     (set up in the Dockerfile), so `ipykernel install --user` needs it.
#   - .config/git: `git config --global` fails if the parent directory of
#     GIT_CONFIG_GLOBAL does not exist.
#   - tools/bin: on PATH for user-provided binaries.
# Non-fatal on failure, like the steps above.
# -------------------------------------------------------------------------
PD="${PD:-/home/jovyan/pd}"
mkdir -p "$PD/jupyter/kernels" "$(dirname "${GIT_CONFIG_GLOBAL:-$PD/.config/git/config}")" "$PD/tools/bin" 2>/dev/null \
    || echo "WARNING: could not create persistent directories under $PD"

# -------------------------------------------------------------------------
# STEP 3: SANITIZE KUBERNETES / GEN3 STORAGE ARGUMENTS
# -------------------------------------------------------------------------
if [ "$1" = "start-notebook.sh" ]; then
    shift
fi

# -------------------------------------------------------------------------
# STEP 4: DETECT RUNTIME MODE (PRODUCTION VS LOCAL TESTING)
# -------------------------------------------------------------------------
if [ $# -eq 0 ] || [[ "$1" == --* ]]; then
    # MODE A: PRODUCTION MODE (Gen3 Environment)
    exec /jupyterlab-start.sh "$@"
else
    # MODE B: TESTING MODE (Local Desktop / Manual Debugging)
    exec "$@"
fi
