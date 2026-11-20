# Server-wide Jupyter config for the Gen3 generic JupyterLab image. Installed at
# /etc/jupyter/jupyter_server_config.py, which Jupyter always reads (also in child
# images that set JUPYTER_CONFIG_PATH).
#
# Kernels from the software library
# ---------------------------------
# The Dockerfile sets JUPYTER_PATH=/apps/jupyter, so JupyterLab also looks for kernel
# specs in /apps/jupyter/kernels/<name>/kernel.json, next to its own kernels. Every
# kernel found there is enabled. Don't set c.KernelSpecManager.kernel_dirs here: that
# replaces the default list (dropping the image's own kernels), and jupyter-lmod
# recomputes kernel_dirs from JUPYTER_PATH after every `module load`, so the env var is
# the mechanism that survives.
#
# A child image can hide kernels by name with a comma-separated list:
#     ENV GEN3_DISABLED_KERNELS="r4.5.2,python3.14"
# Names are the kernel directory names in lowercase (`jupyter kernelspec list`).
import os

from jupyter_client.kernelspec import KernelSpecManager


class Gen3KernelSpecManager(KernelSpecManager):
    """KernelSpecManager that hides the kernels named in $GEN3_DISABLED_KERNELS."""

    def find_kernel_specs(self):
        disabled = {
            name.strip().lower()
            for name in os.environ.get("GEN3_DISABLED_KERNELS", "").split(",")
            if name.strip()
        }
        specs = super().find_kernel_specs()
        hidden = sorted(disabled & set(specs))
        if hidden:
            self.log.info("Hiding kernels disabled by GEN3_DISABLED_KERNELS: %s", ", ".join(hidden))
        return {name: path for name, path in specs.items() if name not in disabled}


c.ServerApp.kernel_spec_manager_class = Gen3KernelSpecManager
