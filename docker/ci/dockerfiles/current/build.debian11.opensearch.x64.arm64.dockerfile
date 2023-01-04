# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for assembling the DEB version of OpenSearch/OpenSearch-Dashboards
# This is not capable of building k-NN plugin as it lacks the necessary old version of glibc on CentOS7

FROM debian:11

ARG DEBIAN_FRONTEND=noninteractive

# Install python37 dependencies
# If keyserver have connectivity issues use 80 port
RUN apt-get update -y && apt install -y gnupg && \
    gpg --keyserver keyserver.ubuntu.com --recv-keys F23C5A6CF475977595C89F51BA6932366A755776 && \
    gpg --export F23C5A6CF475977595C89F51BA6932366A755776 | tee /usr/share/keyrings/ppa-deadsnakes.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/ppa-deadsnakes.gpg] http://ppa.launchpad.net/deadsnakes/ppa/ubuntu focal main" > /etc/apt/sources.list.d/ppa-deadsnakes.list

# Install python37 binaries
RUN apt-get update -y && apt-get install -y python3.7-full && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1

# Install necessary packages
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y docker.io curl build-essential git jq && \
    apt-get install -y debmake debhelper-compat && \
    apt-get clean -y

# Install pip packages
RUN curl -SL https://bootstrap.pypa.io/get-pip.py | python && \
    pip3 install pipenv && pipenv --version && \
    pip3 install awscli==1.22.12 && aws --version

# Tools setup
COPY --chown=0:0 config/jdk-setup.sh config/yq-setup.sh /tmp/
RUN /tmp/jdk-setup.sh && /tmp/yq-setup.sh

# Create user group
RUN groupadd -g 1000 opensearch && \
    useradd -u 1000 -g 1000 -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R 1000:1000 /usr/share/opensearch 

# Install gh cli
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=`dpkg --print-architecture` signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list && \
    apt-get update && apt-get install -y gh && apt-get clean

# Change User
USER 1000
WORKDIR /usr/share/opensearch
