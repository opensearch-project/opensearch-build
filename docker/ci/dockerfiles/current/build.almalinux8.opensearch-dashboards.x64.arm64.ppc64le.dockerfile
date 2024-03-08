# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for standardize the ci/cd environment
# for both developers and ci/cd tools in OpenSearch / OpenSearch-Dashboards
# Please read the README.md file for all the information before using this dockerfile

FROM almalinux:8

ARG CONTAINER_USER=ci-runner
ARG CONTAINER_USER_HOME=/home/ci-runner

# Ensure localedef running correct with root permission
USER 0

# Add normal dependencies
RUN dnf clean all && dnf install -y 'dnf-command(config-manager)' && \
    dnf config-manager --set-enabled powertools && \
    dnf install epel-release -y && dnf repolist && \
    dnf update -y && \
    dnf install -y which curl git gnupg2 tar net-tools procps-ng python39 python39-devel python39-pip zip unzip jq

# Create user group
RUN groupadd -g 1000 $CONTAINER_USER && \
    useradd -u 1000 -g 1000 -d $CONTAINER_USER_HOME $CONTAINER_USER && \
    mkdir -p $CONTAINER_USER_HOME && \
    chown -R 1000:1000 $CONTAINER_USER_HOME

# Add Python dependencies
RUN dnf install -y @development zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel findutils

# Add Dashboards dependencies
RUN dnf install -y xorg-x11-server-Xvfb gtk2-devel gtk3-devel libnotify-devel GConf2 nss libXScrnSaver alsa-lib

# Add Notebook dependencies
RUN dnf install -y nss xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-utils xorg-x11-fonts-cyrillic xorg-x11-fonts-Type1 xorg-x11-fonts-misc fontconfig freetype && dnf clean all

# Add Yarn dependencies
RUN dnf groupinstall -y "Development Tools" && dnf clean all && rm -rf /var/cache/dnf/*

# Tools setup
COPY --chown=0:0 config/yq-setup.sh config/gh-setup.sh /tmp/
RUN dnf install -y go && /tmp/yq-setup.sh && /tmp/gh-setup.sh

# Setup Shared Memory
RUN chmod -R 777 /dev/shm

# Install PKG builder dependencies with rvm
RUN curl -sSL https://rvm.io/mpapis.asc | gpg2 --import - && \
    curl -sSL https://rvm.io/pkuczynski.asc | gpg2 --import - && \
    curl -sSL https://get.rvm.io | bash -s stable

# Switch shell for rvm related commands
SHELL ["/bin/bash", "-lc"]

# Install ruby / rpm / fpm related dependencies
RUN . /etc/profile.d/rvm.sh && rvm install 2.6.0 && rvm --default use 2.6.0 && dnf install -y rpm-build createrepo && dnf clean all

ENV RUBY_HOME=/usr/local/rvm/rubies/ruby-2.6.0/bin
ENV RVM_HOME=/usr/local/rvm/bin
ENV GEM_HOME=$CONTAINER_USER_HOME/.gem
ENV GEM_PATH=$GEM_HOME
ENV PATH=$RUBY_HOME:$RVM_HOME:$PATH

# Install Python binary
RUN update-alternatives --set python /usr/bin/python3.9 && \
    update-alternatives --set python3 /usr/bin/python3.9 && \
    pip3 install pip==23.1.2 && pip3 install pipenv==2023.6.12 awscli==1.32.17

# Preparation for awscliv2
#RUN pip3 install git+https://github.com/aws/aws-cli.git@2.11.17
#ENV AWS_CLI_FILE_ENCODING=UTF-8

# Change User
USER $CONTAINER_USER
WORKDIR $CONTAINER_USER_HOME

# Install fpm for opensearch dashboards core
RUN gem install dotenv -v 2.8.1 && gem install fpm -v 1.14.2
ENV PATH=$CONTAINER_USER_HOME/.gem/gems/fpm-1.14.2/bin:$PATH

# Hard code node version and yarn version for now
# nvm environment variables
ENV NVM_DIR $CONTAINER_USER_HOME/.nvm
ENV NODE_VERSION 10.24.1
ARG NODE_VERSION_LIST="10.24.1 14.19.1 14.20.0 14.20.1 14.21.3 16.20.0 18.16.0 18.19.0"
# install nvm
# https://github.com/creationix/nvm#install-script
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
# install node and npm
COPY --chown=$CONTAINER_USER:$CONTAINER_USER config/yarn-version.sh /tmp
RUN source $NVM_DIR/nvm.sh && \
    for node_version in $NODE_VERSION_LIST; do nvm install $node_version; npm install -g yarn@`/tmp/yarn-version.sh main`; done
# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH
# We use the version test to check if packages installed correctly
# And get added to the PATH
# This will fail the docker build if any of the packages not exist
RUN node -v
RUN npm -v
RUN yarn -v
RUN fpm -v
