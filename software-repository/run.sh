#!/usr/bin/env bash

# Run with -l for local apps mountpoint.

export APPS_PATH=~/.gen3/workspaces/apps
export REPO_PATH=~/git/github/uc-cdis/containers

while getopts "l" opt; do
case $opt in
  l)
    LOCAL=true
    ;;
  esac
done

if [ "$LOCAL" = true ] ; then
  docker run -d \
    -it \
    --name gen3-workspace-admin \
    --mount type=bind,source=${APPS_PATH},target=/apps \
    --mount type=bind,source=${REPO_PATH}/software-repository/spack,target=/spack \
    gen3-workspace-admin
else
  docker run -d \
    -it \
    --name gen3-workspace-admin \
    --mount type=bind,source=${REPO_PATH}/software-repository/spack,target=/spack \
    --env-file <(aws configure export-credentials --profile workspacesresearch_planx-707767160287 --format env-no-export) \
    --device /dev/fuse \
    --privileged \
    gen3-workspace-admin
fi
