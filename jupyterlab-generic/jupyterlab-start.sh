#!/usr/bin/env bash

# Symlink config files for persistence
if [[ -d "./pd " ]]; then
    test -f ./pd/.bash_profile || touch ./pd/.bash_profile
    test -f ./pd/.bashrc || touch ./pd/.bashrc
    test -d ./pd/.jupyter || mkdir ./pd/.jupyter
    test -d ./pd/.ipython || mkdir ./pd/.ipython
    test -d ./pd/.config || mkdir ./pd/.config
    test -d ./pd/.local || mkdir ./pd/.local
    test -d ./pd/.R || mkdir ./pd/.R
    test -d ./pd/.ado || mkdir ./pd/.ado
    ln -s ./pd/.bash_profile .
    ln -s ./pd/.bashrc .
    ln -s ./pd/.jupyter .
    ln -s ./pd/.ipython .
    ln -s ./pd/.config .
    ln -s ./pd/.local .
    ln -s ./pd/R .
    ln -s ./pd/ado .
fi

# Check if LMOD default modules has been set
if [[ -z "$LMOD_SYSTEM_DEFAULT_MODULES" ]]; then
    echo "Setting LMOD default modules"
    export LMOD_SYSTEM_DEFAULT_MODULES="py-numpy:py-pandas:py-matplotlib:py-scikit-learn:py-heal-sdk:py-gen3"
fi

# Load JupyterLab extension dependencies
source /apps/lmod/lmod/init/profile

have_defaults=1
IFS=':' read -r -a default_modules <<< "$LMOD_SYSTEM_DEFAULT_MODULES"
echo "Checking for default modules: ${default_modules[@]}"
for default_module in "${default_modules[@]}"; do
    module is-loaded "$default_module" >/dev/null 2>&1 || have_defaults=0
done
# similar to https://lmod.readthedocs.io/en/latest/070_standard_modules.html
if [ "$have_defaults" -eq 1 ]; then
    echo "Running module refresh"
    module refresh
else
    echo "Running module restore"
    module --initial_load --no_redirect restore
fi

module load git ripgrep

/home/jovyan/.local/bin/jupyter lab \
    --ServerApp.ip=0.0.0.0 \
    --KernelSpecManager.ensure_native_kernel=False \
    --ServerApp.quit_button=False \
    --IdentityProvider.token="" \
    "$@"
