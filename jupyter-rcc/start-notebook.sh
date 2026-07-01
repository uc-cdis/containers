#!/bin/bash
set -e  # Exit instantly if any single setup command fails

# -------------------------------------------------------------------------
# STEP 1: RESTORE TERMINAL ENVIRONMENT & AUTOCOMPLETION
# -------------------------------------------------------------------------
if [ ! -f "/home/jovyan/.bashrc" ]; then
    cp /etc/skel/.bash* /home/jovyan/ 2>/dev/null || true
fi

# -------------------------------------------------------------------------
# STEP 2: SANITIZE KUBERNETES / GEN3 STORAGE ARGUMENTS
# -------------------------------------------------------------------------
if [ "$1" = "start-notebook.sh" ]; then
    shift
fi

# -------------------------------------------------------------------------
# STEP 3: DETECT RUNTIME MODE (PRODUCTION VS LOCAL TESTING)
# -------------------------------------------------------------------------
if [ $# -eq 0 ] || [[ "$1" == --* ]]; then
    # MODE A: PRODUCTION MODE (Gen3 Environment)
    exec jupyter lab "$@"
else
    # MODE B: TESTING MODE (Local Desktop / Manual Debugging)
    exec "$@"
fi
