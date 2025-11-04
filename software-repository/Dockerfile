# For administering software used in Gen3 workspaces

FROM public.ecr.aws/amazonlinux/amazonlinux:2023
# See Spack prereqs here: https://spack.readthedocs.io/en/latest/installing_prerequisites.html
RUN dnf upgrade --refresh && \
    dnf install -y file bzip2 ca-certificates git gzip patch python3 tar unzip xz zstd gcc gcc-c++ gcc-gfortran procps

COPY resources/spack/config.yaml /etc/spack/.
COPY resources/spack/modules.yaml /etc/spack/.
COPY resources/lmod/.modulerc.lua /root/lmod/.

ENTRYPOINT ["/bin/bash"]
