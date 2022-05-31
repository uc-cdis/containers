#!/bin/bash
if [[ -z "${STATA_LICENSE}" ]]; then
  echo "STATA_LICENSE unset. exiting..."
  exit 1
else
  echo $STATA_LICENSE > /usr/local/stata17/stata.lic
  unset STATA_LICENSE
  start-notebook.sh --NotebookApp.nbserver_extensions="{'custom_api.ready_handler':True}" $NOTEBOOK_ARGS $@ &
  JUPYTER_PID=$!
  sleep 10
  # python3 /tmp/setup_notebooks.py

  # echo "Deleting local copy of Stata license..."
  # rm /usr/local/stata17/stata.lic

  # echo "Signaling that Jupyter is ready to serve..."
  # touch /tmp/ready
  wait $JUPYTER_PID
fi
