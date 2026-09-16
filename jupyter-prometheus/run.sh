#!/usr/bin/env bash

/home/jovyan/.local/bin/jupyter lab \
    --ServerApp.ip=0.0.0.0 \
    --KernelSpecManager.ensure_native_kernel=False \
    --ServerApp.quit_button=False \
    --IdentityProvider.token="" \
    "$@"
