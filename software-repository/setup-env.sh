#!/usr/bin/env bash

git clone https://github.com/s3fs-fuse/s3fs-fuse.git
cd s3fs-fuse
./autogen.sh
./configure --prefix=/usr --with-openssl
make
make install

mkdir /apps
s3fs workspace-software-s3-qa-brh /apps

source /spack/share/spack/setup-env.sh
