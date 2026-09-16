#!/bin/bash
set -e  # Exit instantly if any single setup command fails

/home/jovyan/.local/bin/jupyter lab \
    --KernelSpecManager.ensure_native_kernel=False \
    --IdentityProvider.token="" \
    "$@"
