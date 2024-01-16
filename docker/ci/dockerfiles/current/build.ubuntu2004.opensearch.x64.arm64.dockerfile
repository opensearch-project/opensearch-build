# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for assembling the DEB version of OpenSearch/OpenSearch-Dashboards
# This is not capable of building k-NN plugin as it lacks the necessary old version of glibc on CentOS7

FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ARG CONTAINER_USER=ci-runner
ARG CONTAINER_USER_HOME=/home/ci-runner

# Install python dependencies
RUN apt-get update -y && apt-get install -y software-properties-common

# Install python binaries
RUN apt-get update -y && apt-get install python3 && \
    apt-get install -y python3.9-full python3.9-dev && \
    apt-get install -y python-is-python3 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# Install necessary packages
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y docker.io curl build-essential git jq && \
    apt-get install -y debmake debhelper-compat && \
    apt-get install -y libxrender1 libxtst6 libasound2 libxi6 libgconf-2-4 && \
    apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libatspi2.0-dev libxcomposite-dev libxdamage1 libxfixes3 libxfixes-dev libxrandr2 libgbm-dev libxkbcommon-x11-0 libpangocairo-1.0-0 libcairo2 libcairo2-dev libnss3 libnspr4 libnspr4-dev freeglut3 && \
    apt-get clean -y

# Install pip packages
RUN curl -SL https://bootstrap.pypa.io/get-pip.py | python && \
    pip3 install pip==23.1.2 && pip3 install pipenv==2023.6.12 awscli==1.32.17 docker-compose==1.29.2

# Install aptly and required changes to debmake
# Remove lintian for now due to it takes nearly 20 minutes for OpenSearch as well as nearly an hour for OpenSearch-Dashboards during debmake
RUN curl -o- https://www.aptly.info/pubkey.txt | apt-key add - && \
    echo "deb http://repo.aptly.info/ squeeze main" | tee -a /etc/apt/sources.list.d/aptly.list && \
    apt-get update -y && apt-get install -y aptly && apt-get clean -y && \
    dpkg -r lintian

# Tools setup
COPY --chown=0:0 config/jdk-setup.sh config/yq-setup.sh /tmp/
RUN /tmp/jdk-setup.sh && /tmp/yq-setup.sh # Ubuntu has a bug where entrypoint=bash does not actually run .bashrc correctly

# Create user group
RUN groupadd -g 1000 $CONTAINER_USER && \
    useradd -u 1000 -g 1000 -s /bin/bash -d $CONTAINER_USER_HOME -m $CONTAINER_USER && \
    mkdir -p $CONTAINER_USER_HOME && \
    chown -R 1000:1000 $CONTAINER_USER_HOME

# Install gh cli
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=`dpkg --print-architecture` signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list && \
    apt-get update && apt-get install -y gh && apt-get clean

# Change User
USER $CONTAINER_USER
WORKDIR $CONTAINER_USER_HOME
