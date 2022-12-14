# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for assembling the DEB version of OpenSearch/OpenSearch-Dashboards
# This is not capable of building k-NN plugin as it lacks the necessary old version of glibc on CentOS7

FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y docker.io curl python3 python3-pip build-essential jq && \
    apt-get install -y debmake debhelper-compat && \
    apt-get clean -y

## Install python37 dependencies
#RUN apt-get install -y libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev
#
## Install Python37 binary
#RUN curl https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz | tar xzvf - && \
#    cd Python-3.7.7 && \
#    ./configure --enable-optimizations && \
#    make altinstall
#
## Setup Python37 links
#RUN ln -sfn /usr/local/bin/python3.7 /usr/bin/python3 && \
#    ln -sfn /usr/local/bin/pip3.7 /usr/bin/pip && \
#    ln -sfn /usr/local/bin/pip3.7 /usr/local/bin/pip && \
#    ln -sfn /usr/local/bin/pip3.7 /usr/bin/pip3 && \
#    ln -sfn /usr/share/pyshared/lsb_release.py /usr/local/lib/python3.7/site-packages/lsb_release.py && \
#    pip3 install pipenv && pipenv --version
#
## More pip installation
#RUN pip3 install pip==21.3.1
#RUN pip3 install awscli==1.22.12

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
