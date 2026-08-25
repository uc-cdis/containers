#!/usr/bin/env bash
export APPS_PATH=~/.gen3/workspaces/apps
export PD_PATH=~/.gen3/workspaces/pd
export DATA_PATH=~/.gen3/workspaces/data
docker run -d \
  -it \
  --name jupyterlab-generic \
  -p 8888:8888 \
  --mount type=bind,source=${APPS_PATH},target=/apps,readonly \
  --mount type=bind,source=${PD_PATH},target=/home/jovyan/pd \
  --mount type=bind,source=${DATA_PATH},target=/data \
  jupyterlab-generic
