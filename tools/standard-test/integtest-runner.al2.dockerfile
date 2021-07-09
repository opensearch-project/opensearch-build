# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.


# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.

# This is a docker image specifically for standardize the test environment
# for both developers and ci/cd tools in OpenSearch

# You must run these commands on the LINUX host for OpenSearch process to run
# sudo sysctl -w vm.max_map_count=262144
# ulimit -n 65535

# You must make this edit on the LINUX host and restart docker deamon for OpenSearch process to run
# As well as running Dashboards integtest so headless chrome will not crash
# Edit /etc/sysconfig/docker to have nofiles to 65535, and default shared memory to 1024MiB
# OPTIONS="--default-ulimit nofile=65535:65535 --default-shm-size 1024000000"
# sudo systemctl stop docker
# sudo systemctl start docker

# You must change docker memory/RAM utilization in resources settings if you use Docker Desktop on macOS
# Make sure at least 4GiB of RAM is used, so Dashboards process can startup correctly


FROM amazonlinux:2

# Add AdoptOpenJDK Repo
RUN echo -e "[AdoptOpenJDK]\nname=AdoptOpenJDK\nbaseurl=http://adoptopenjdk.jfrog.io/adoptopenjdk/rpm/centos/7/\$basearch\nenabled=1\ngpgcheck=1\ngpgkey=https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public" > /etc/yum.repos.d/adoptopenjdk.repo

# Add normal dependencies
RUN yum update -y && \
    yum install -y adoptopenjdk-14-hotspot which curl python git tar net-tools procps-ng

# Add Dashboards dependencies
RUN yum install -y xorg-x11-server-Xvfb gtk2-devel gtk3-devel libnotify-devel GConf2 nss libXScrnSaver alsa-lib

# Add Notebook dependencies
RUN yum install -y libnss3.so xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-utils xorg-x11-fonts-cyrillic xorg-x11-fonts-Type1 xorg-x11-fonts-misc fontconfig freetype && yum clean all

# Add Yarn dependencies
RUN yum groupinstall -y "Development Tools"

# Remove yum cache so that docker images size reduces 300 to 400MiB
RUN yum clean all && rm -rf /var/cache/yum/*

# Setup Shared Memory
RUN chmod -R 777 /dev/shm

# Create user group
RUN groupadd -g 1000 opensearch && \
    useradd -u 1000 -g 1000 -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R 1000:1000 /usr/share/opensearch

# Set JAVA_HOME
# AdoptOpenJDK apparently does not add JAVA_HOME after installation
RUN echo "export JAVA_HOME=`dirname $(dirname $(readlink -f $(which javac)))`" >> /etc/profile.d/java_home.sh

# Change User
USER 1000
WORKDIR /usr/share/opensearch

# Hard code node version and yarn version for now
# nvm environment variables
ENV NVM_DIR /usr/share/opensearch/.nvm
ENV NODE_VERSION 10.24.1
# install nvm
# https://github.com/creationix/nvm#install-script
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.2/install.sh | bash
# install node and npm
RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default
# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH
# install yarn
RUN npm install -g yarn@^1.21.1
# install cypress
RUN npm install -g cypress@^6.9.1 && npm cache verify
# We use the version test to check if packages installed correctly
# And get added to the PATH
# This will fail the docker build if any of the packages not exist
RUN node -v
RUN npm -v
RUN yarn -v
RUN cypress -v
