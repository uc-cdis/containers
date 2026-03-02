#!/usr/bin/env bash

_timeit() {
    local label="$1"; shift
    local start end elapsed
    start=$(date +%s%3N)
    "$@"
    local rc=$?
    end=$(date +%s%3N)
    elapsed=$(( end - start ))
    echo "[TIMER] ${label}: ${elapsed}ms" >&2
    return $rc
}

_timeit "touch .bash_profile"  bash -c 'test -f ./pd/.bash_profile || touch ./pd/.bash_profile'
_timeit "touch .bashrc"        bash -c 'test -f ./pd/.bashrc       || touch ./pd/.bashrc'
_timeit "mkdir .jupyter"       bash -c 'test -d ./pd/.jupyter      || mkdir ./pd/.jupyter'
_timeit "mkdir .ipython"       bash -c 'test -d ./pd/.ipython      || mkdir ./pd/.ipython'
_timeit "mkdir .config"        bash -c 'test -d ./pd/.config       || mkdir ./pd/.config'
_timeit "mkdir .local"         bash -c 'test -d ./pd/.local        || mkdir ./pd/.local'

_timeit "ln .bash_profile"     ln -s ./pd/.bash_profile .
_timeit "ln .bashrc"           ln -s ./pd/.bashrc .
_timeit "ln .jupyter"          ln -s ./pd/.jupyter .
_timeit "ln .ipython"          ln -s ./pd/.ipython .
_timeit "ln .config"           ln -s ./pd/.config .
_timeit "ln .local"            ln -s ./pd/.local .

_timeit "source lmod profile"  bash -c 'source /apps/lmod/lmod/init/profile'
_timeit "module load git"      bash -c 'source /apps/lmod/lmod/init/profile && module load git'
# module load ripgrep
_timeit "module load py-pandas" bash -c 'source /apps/lmod/lmod/init/profile && module load py-pandas'
# module load py-scipy

echo "[TIMER] Starting jupyter lab..." >&2
_timeit "jupyter lab (startup)" \
    /usr/local/python-venv/bin/jupyter lab \
        --ServerApp.ip=0.0.0.0 \
        --KernelSpecManager.ensure_native_kernel=False \
        --ServerApp.quit_button=False \
        --IdentityProvider.token="" \
        "$@"
