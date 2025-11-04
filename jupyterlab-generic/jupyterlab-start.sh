#!/usr/bin/env bash

# Symlink config files for persistence
test -f ./pd/.bash_profile || touch ./pd/.bash_profile
test -f ./pd/.bashrc || touch ./pd/.bashrc
test -d ./pd/.jupyter || mkdir ./pd/.jupyter
test -d ./pd/.ipython || mkdir ./pd/.ipython
test -d ./pd/.config || mkdir ./pd/.config
test -d ./pd/.local || mkdir ./pd/.local
ln -s ./pd/.bash_profile .
ln -s ./pd/.bashrc .
ln -s ./pd/.jupyter .
ln -s ./pd/.ipython .
ln -s ./pd/.config .
ln -s ./pd/.local .

# Symlink data directory mounted at root
ln -s /data .

# Load JupyterLab extension dependencies
source /apps/lmod/lmod/init/profile
module load git ripgrep
# Load default modules
module load py-pandas py-scipy

/usr/local/python-venv/bin/jupyter lab \
    --ip=0.0.0.0 \
    --KernelSpecManager.ensure_native_kernel=False \
    --ServerApp.quit_button=False \
    --IdentityProvider.token=""
