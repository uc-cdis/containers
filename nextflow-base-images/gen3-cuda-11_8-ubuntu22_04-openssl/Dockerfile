# Use the specified base image
FROM nvcr.io/nvidia/cuda:11.8.0-base-ubuntu22.04

RUN apt-get purge -y --auto-remove openssl && apt-get autoremove && apt-get autoclean

# RUN apt-get update && apt-get -y upgrade && apt install -y wget

# RUN apt install -y build-essential && \
#     apt-get install -y python3 && \
#     apt-get install -y python3-pip

# # install openssl 3.0.8 as it is required for FIPS compliance.
# WORKDIR /tmp
# RUN wget https://www.openssl.org/source/openssl-3.0.8.tar.gz && \
#     tar -xzvf openssl-3.0.8.tar.gz && \
#     rm openssl-3.0.8.tar.gz

# WORKDIR /tmp/openssl-3.0.8
# RUN ./Configure enable-fips && \
#     make && \
#     make install

# # Changing adding `/usr/local/lib` as a prefix to LD_LIBRARY_PATH will
# # give precedence to OpenSSL 3.0.8 library files over the 3.0.2
# ENV LD_LIBRARY_PATH=/usr/local/lib:/usr/local/lib64:$LD_LIBRARY_PATH

# # Make config changes ti ensure FIPS compliance
# RUN sed -i 's$# .include fipsmodule.cnf$.include /usr/local/ssl/fipsmodule.cnf$g' /usr/local/ssl/openssl.cnf
# RUN sed -i 's$providers = provider_sect$providers = provider_sect\nalg_section = algorithm_sect$g' /usr/local/ssl/openssl.cnf
# RUN sed -i 's$# fips = fips_sect$fips = fips_sect$g' /usr/local/ssl/openssl.cnf
# RUN sed -i -e 's$# activate = 1$activate = 1 \n\n[algorithm_sect]\ndefault_properties = fips=yes$g' /usr/local/ssl/openssl.cnf


# # Clean up the temporary directory
# WORKDIR /
# RUN rm -rf /tmp/openssl-3.0.8
RUN echo "Uncomment whole doc and remove this Echo before merging the PR"
