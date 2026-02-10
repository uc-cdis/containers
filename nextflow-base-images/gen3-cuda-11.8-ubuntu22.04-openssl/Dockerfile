# Use the specified base image
FROM nvcr.io/nvidia/cuda:11.8.0-base-ubuntu22.04 AS openssl-builder

# Install build deps only
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        wget \
        ca-certificates && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /tmp
RUN wget https://www.openssl.org/source/openssl-3.0.8.tar.gz && \
    tar -xzf openssl-3.0.8.tar.gz

WORKDIR /tmp/openssl-3.0.8
RUN ./Configure enable-fips && make -j$(nproc) && make install_sw install_ssldirs

FROM nvcr.io/nvidia/cuda:11.8.0-base-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive

# Install runtime deps only
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        python3 \
        python3-pip \
        libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Copy OpenSSL runtime artifacts only
COPY --from=openssl-builder /usr/local/ssl /usr/local/ssl
COPY --from=openssl-builder /usr/local/lib /usr/local/lib
COPY --from=openssl-builder /usr/local/lib64 /usr/local/lib64
COPY --from=openssl-builder /usr/local/bin/openssl /usr/local/bin/openssl

ENV LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64:$LD_LIBRARY_PATH
ENV OPENSSL_CONF=/usr/local/ssl/openssl.cnf

# FIPS config
RUN sed -i 's$# .include fipsmodule.cnf$.include /usr/local/ssl/fipsmodule.cnf$g' /usr/local/ssl/openssl.cnf && \
    sed -i 's$providers = provider_sect$providers = provider_sect\nalg_section = algorithm_sect$g' /usr/local/ssl/openssl.cnf && \
    sed -i 's$# fips = fips_sect$fips = fips_sect$g' /usr/local/ssl/openssl.cnf && \
    sed -i -e 's$# activate = 1$activate = 1 \n\n[algorithm_sect]\ndefault_properties = fips=yes$g' /usr/local/ssl/openssl.cnf
WORKDIR /
