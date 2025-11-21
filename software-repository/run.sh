#!/usr/bin/env bash
export APPS_PATH=~/.gen3/workspaces/apps
export REPO_PATH=~/git/github/uc-cdis/containers
docker run -d \
  -it \
  --name gen3-workspace-admin \
  --mount type=bind,source=${APPS_PATH},target=/apps \
  --mount type=bind,source=${REPO_PATH}/software-repository/spack,target=/spack \
  gen3-workspace-admin
