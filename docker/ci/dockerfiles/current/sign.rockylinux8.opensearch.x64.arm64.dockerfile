# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for running the signing workflow
# Either for OpenSearchSignerClient or for RPM Signing

FROM rockylinux:8

ARG MAVEN_DIR=/usr/local/apache-maven

# Ensure localedef running correct with root permission
USER 0

# Setup ENV to prevent ASCII data issues with Python3
RUN echo "export LC_ALL=en_US.utf-8" >> /etc/profile.d/python3_ascii.sh && \
    echo "export LANG=en_US.utf-8" >> /etc/profile.d/python3_ascii.sh && \
    localedef -v -c -i en_US -f UTF-8 en_US.UTF-8 || echo set locale

# Add normal dependencies
RUN dnf clean all && \
    dnf update -y && \
    dnf install -y which curl git gnupg2 tar net-tools procps-ng python3 python3-devel python3-pip zip unzip

# Create user group
RUN groupadd -g 1000 opensearch && \
    useradd -u 1000 -g 1000 -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R 1000:1000 /usr/share/opensearch

# Add Python37 dependencies
RUN dnf install -y @development zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel \
                   libffi-devel findutils rpm-build createrepo pinentry rpm-sign gnupg2

# Install Python37 binary
RUN curl https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz | tar xzvf - && \
    cd Python-3.7.7 && \
    ./configure --enable-optimizations && \
    make altinstall

# Setup Python37 links
RUN ln -sfn /usr/local/bin/python3.7 /usr/bin/python3 && \
    ln -sfn /usr/local/bin/pip3.7 /usr/bin/pip && \
    ln -sfn /usr/local/bin/pip3.7 /usr/local/bin/pip && \
    ln -sfn /usr/local/bin/pip3.7 /usr/bin/pip3 && \
    pip3 install pipenv awscli && pipenv --version

# Change User
USER 1000
WORKDIR /usr/share/opensearch

