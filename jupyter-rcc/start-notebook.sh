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
    exec jupyter lab "$@"
else
    # MODE B: TESTING MODE (Local Desktop / Manual Debugging)
    exec "$@"
fi
