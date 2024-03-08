# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for standardize the ci/cd environment
# for both developers and ci/cd tools in OpenSearch / OpenSearch-Dashboards
# Please read the README.md file for all the information before using this dockerfile

########################### Stage 0 ########################
FROM almalinux:8 AS linux_stage_0

ARG CONTAINER_USER=ci-runner
ARG CONTAINER_USER_HOME=/home/ci-runner

USER 0

# Add normal dependencies
RUN dnf clean all && \
    dnf update -y && \
    dnf install -y which curl git gnupg2 tar net-tools procps-ng python39 python39-devel python39-pip zip unzip

# Add Dashboards dependencies (mainly for cypress)
RUN dnf install -y xorg-x11-server-Xvfb gtk2-devel gtk3-devel libnotify-devel GConf2 nss libXScrnSaver alsa-lib

# Add Yarn dependencies
RUN dnf groupinstall -y "Development Tools" && dnf install -y cmake && dnf clean all && rm -rf /var/cache/dnf/*

# Create user group
RUN groupadd -g 1000 $CONTAINER_USER && \
    useradd -u 1000 -g 1000 -d $CONTAINER_USER_HOME $CONTAINER_USER && \
    mkdir -p $CONTAINER_USER_HOME && \
    chown -R 1000:1000 $CONTAINER_USER_HOME

# install yq
COPY --chown=0:0 config/yq-setup.sh /tmp/
RUN /tmp/yq-setup.sh

# Change User
USER $CONTAINER_USER
WORKDIR $CONTAINER_USER_HOME

# Hard code node version and yarn version for now
# nvm environment variables
ENV NVM_DIR $CONTAINER_USER_HOME/.nvm
ENV NODE_VERSION 18.19.0
ENV CYPRESS_VERSION 12.13.0
ARG CYPRESS_VERSION_LIST="5.6.0 9.5.4 12.13.0"
ENV CYPRESS_LOCATION $CONTAINER_USER_HOME/.cache/Cypress/$CYPRESS_VERSION
ENV CYPRESS_LOCATION_954 $CONTAINER_USER_HOME/.cache/Cypress/9.5.4
# install nvm
# https://github.com/creationix/nvm#install-script
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
# install node and npm
RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default
# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH
# install yarn
COPY --chown=$CONTAINER_USER:$CONTAINER_USER config/yarn-version.sh /tmp
RUN npm install -g yarn@`/tmp/yarn-version.sh main`
# Add legacy cypress@5.6.0 for 1.x line
# Add legacy cypress@9.5.4 for pre-2.8.0 releases
# Add latest cypress@12.13.0 for post-2.8.0 releases
RUN for cypress_version in $CYPRESS_VERSION_LIST; do npm install -g cypress@$cypress_version && npm cache verify; done

# Need root to get pass the build due to chrome sandbox needs to own by the root
USER 0

# Add legacy cypress 5.6.0 / 9.5.4 for ARM64 Architecture
RUN if [ `uname -m` = "aarch64" ]; then for cypress_version in 5.6.0 9.5.4; do rm -rf $CONTAINER_USER_HOME/.cache/Cypress/$cypress_version && \
    curl -SLO https://ci.opensearch.org/ci/dbc/tools/Cypress-$cypress_version-arm64.tar.gz && tar -xzf Cypress-$cypress_version-arm64.tar.gz -C $CONTAINER_USER_HOME/.cache/Cypress/ && \
    chown $CONTAINER_USER:$CONTAINER_USER -R $CONTAINER_USER_HOME/.cache/Cypress/$cypress_version && rm -vf Cypress-$cypress_version-arm64.tar.gz; done; fi

########################### Stage 1 ########################
FROM almalinux:8

ARG CONTAINER_USER=ci-runner
ARG CONTAINER_USER_HOME=/home/ci-runner

USER 0

# Add normal dependencies
RUN dnf clean all && dnf install -y 'dnf-command(config-manager)' && \
    dnf update -y && \
    dnf install -y which curl git gnupg2 tar net-tools procps-ng python39 python39-devel python39-pip zip unzip

# Create user group
RUN groupadd -g 1000 $CONTAINER_USER && \
    useradd -u 1000 -g 1000 -d $CONTAINER_USER_HOME $CONTAINER_USER && \
    mkdir -p $CONTAINER_USER_HOME && \
    chown -R 1000:1000 $CONTAINER_USER_HOME

# Copy from Stage0
COPY --from=linux_stage_0 --chown=$CONTAINER_USER:$CONTAINER_USER $CONTAINER_USER_HOME $CONTAINER_USER_HOME
ENV NVM_DIR $CONTAINER_USER_HOME/.nvm
ENV NODE_VERSION 18.19.0
ENV CYPRESS_VERSION 12.13.0
ENV CYPRESS_LOCATION $CONTAINER_USER_HOME/.cache/Cypress/$CYPRESS_VERSION
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# Check dirs
RUN source $NVM_DIR/nvm.sh && ls -al $CONTAINER_USER_HOME && echo $NODE_VERSION $NVM_DIR && nvm use $NODE_VERSION

# Add Python dependencies
RUN dnf install -y @development zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel findutils

# Add Dashboards dependencies (mainly for cypress)
RUN dnf install -y xorg-x11-server-Xvfb gtk2-devel gtk3-devel libnotify-devel GConf2 nss libXScrnSaver alsa-lib

# Add Reports dependencies
RUN dnf install -y nss xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-utils xorg-x11-fonts-cyrillic xorg-x11-fonts-Type1 xorg-x11-fonts-misc fontconfig freetype

# Add Yarn dependencies
RUN dnf groupinstall -y "Development Tools" && dnf clean all && rm -rf /var/cache/dnf/*

# Setup Shared Memory
RUN chmod -R 777 /dev/shm

# Install Python binary
RUN update-alternatives --set python /usr/bin/python3.9 && \
    update-alternatives --set python3 /usr/bin/python3.9 && \
    pip3 install pip==23.1.2 && pip3 install pipenv==2023.6.12 awscli==1.32.17

# Add other dependencies
RUN dnf install -y epel-release && dnf clean all && dnf install -y jq && dnf clean all && rm -rf /var/cache/dnf/* && \
    pip3 install cmake==3.23.3

# Tools setup
COPY --chown=0:0 config/yq-setup.sh config/gh-setup.sh /tmp/
RUN dnf install -y go && /tmp/yq-setup.sh && /tmp/gh-setup.sh

# Change User
USER $CONTAINER_USER
WORKDIR $CONTAINER_USER_HOME

# We use the version test to check if packages installed correctly
# And get added to the PATH
# This will fail the docker build if any of the packages not exist
RUN node -v
RUN npm -v
RUN yarn -v
RUN cypress -v
