# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for assembling the DEB version of OpenSearch/OpenSearch-Dashboards
# This is not capable of building k-NN plugin as it lacks the necessary old version of glibc on AL2

FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG CONTAINER_USER=ci-runner
ARG CONTAINER_USER_HOME=/home/ci-runner

# Remove ubuntu user which occupies the 1000 userid and groupid since 23.04
# https://bugs.launchpad.net/cloud-images/+bug/2005129
USER 0
RUN touch /var/mail/ubuntu && chown ubuntu /var/mail/ubuntu && userdel -r ubuntu

# Install python dependencies
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa -y

# Install necessary packages
RUN apt-get update -y && apt-get install -y docker.io=24.0.7* curl build-essential git jq && \
    apt-get install -y debmake debhelper-compat && \
    apt-get install -y libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libnss3 libxss1 xauth xvfb && \
    apt-get install -y libxrender1 libxi6 libxtst6 libasound2t64 && \
    apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libatspi2.0-dev libxcomposite-dev libxdamage1 libxfixes3 libxfixes-dev libxrandr2 libgbm-dev libxkbcommon-x11-0 libpangocairo-1.0-0 libcairo2 libcairo2-dev libnss3 libnspr4 libnspr4-dev && \
    apt-get install -y mandoc less && \
    apt-get clean -y

# Docker Compose v2
RUN mkdir -p /usr/local/lib/docker/cli-plugins && \
    if [ `uname -m` = "x86_64" ] || [ `uname -m` = "amd64" ]; then \
        curl -SfL -o /usr/local/lib/docker/cli-plugins/docker-compose https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-linux-x86_64; \
    elif [ `uname -m` = "aarch64" ] || [ `uname -m` = "arm64" ]; then \
        curl -SfL -o /usr/local/lib/docker/cli-plugins/docker-compose https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-linux-aarch64; \
    elif [ `uname -m` = "ppc64le" ]; then \
        curl -SfL -o /usr/local/lib/docker/cli-plugins/docker-compose https://github.com/docker/compose/releases/download/v2.32.4/docker-compose-linux-ppc64le; \
    else \
        echo "Your system is not supported now" && exit 1; \
    fi; \
    chmod 755 /usr/local/lib/docker/cli-plugins/docker-compose && \
    ln -s /usr/local/lib/docker/cli-plugins/docker-compose /usr/local/bin/docker-compose

# Install python, update awscli to v2 due to lib conflicts on urllib3 v1 vs v2
# 20251024: mismatch versions between 3.9.23 and 3.9.24 on arm64, temporarily force old versions on all python3.9 pkgs
#           https://github.com/deadsnakes/issues/issues/330
RUN if [ `uname -m` = "aarch64" ]; then apt-get update -y && apt-get install -y python3.9-full=3.9.23* python3.9-dev=3.9.23* libpython3.9-testsuite=3.9.23*; \
    else apt-get update -y && apt-get install -y python3.9-full python3.9-dev; fi

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 100 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.9 100 && \
    update-alternatives --set python3 /usr/bin/python3.9 && \
    update-alternatives --set python /usr/bin/python3.9 && \
    curl -SL https://bootstrap.pypa.io/get-pip.py | python3 - && \
    pip3 install awscliv2==2.3.1 pipenv==2023.6.12 && \
    ln -s `which awsv2` /usr/local/bin/aws && aws --install

# Install aptly and required changes to debmake
# Remove lintian for now due to it takes nearly 20 minutes for OpenSearch as well as nearly an hour for OpenSearch-Dashboards during debmake
RUN curl -SfL -o /etc/apt/keyrings/aptly.asc https://www.aptly.info/pubkey.txt && \
    echo "deb [signed-by=/etc/apt/keyrings/aptly.asc] http://repo.aptly.info/release noble main" | tee -a /etc/apt/sources.list.d/aptly.list && \
    apt-get update -y && apt-get install -y aptly=1.5.0* && apt-get clean -y && \
    dpkg -r lintian

# Tools setup
COPY --chown=0:0 config/jdk-setup.sh config/yq-setup.sh config/gh-setup.sh config/op-setup.sh /tmp/
RUN apt-get install -y golang-1.22 && /tmp/jdk-setup.sh && /tmp/yq-setup.sh && /tmp/gh-setup.sh && /tmp/op-setup.sh && apt-get clean -y && apt-get autoremove -y # Ubuntu has a bug where entrypoint=bash does not actually run .bashrc correctly

# Create user group
RUN groupadd -g 1000 $CONTAINER_USER && \
    useradd -u 1000 -g 1000 -s /bin/bash -d $CONTAINER_USER_HOME -m $CONTAINER_USER && \
    mkdir -p $CONTAINER_USER_HOME && \
    chown -R 1000:1000 $CONTAINER_USER_HOME

# Change User
USER $CONTAINER_USER
WORKDIR $CONTAINER_USER_HOME

RUN aws --install

# Install Rust
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- --default-toolchain stable -y

# Install protobuf
RUN if [ "$(uname -m)" = "x86_64" ]; then \
        curl -SfL https://github.com/protocolbuffers/protobuf/releases/download/v33.0/protoc-33.0-linux-x86_64.zip -O protoc.zip; \
    else \
        curl -Sfl https://github.com/protocolbuffers/protobuf/releases/download/v33.0/protoc-33.0-linux-aarch_64.zip -O protoc.zip; \
    fi; \
    unzip protoc.zip -d $CONTAINER_USER_HOME/.local && rm -v protoc.zip

# Setup ENV
ENV PATH=$CONTAINER_USER_HOME/.local/bin:$PATH
RUN protoc --version
