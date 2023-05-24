# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for standardize the ci/cd environment
# for both developers and ci/cd tools in OpenSearch / OpenSearch-Dashboards
# Please read the README.md file for all the information before using this dockerfile

########################### Stage 0 ########################
FROM rockylinux:8 AS linux_stage_0

USER 0

# Add normal dependencies
RUN yum clean all && \
    yum update -y && \
    yum install -y which curl git gnupg2 tar net-tools procps-ng python3 python3-devel python3-pip zip unzip

# Add Dashboards dependencies (mainly for cypress)
RUN yum install -y xorg-x11-server-Xvfb gtk2-devel gtk3-devel libnotify-devel GConf2 nss libXScrnSaver alsa-lib

# Add Yarn dependencies
RUN yum groupinstall -y "Development Tools" && yum install -y cmake && yum clean all && rm -rf /var/cache/yum/*

# Create user group
RUN groupadd -g 1000 opensearch && \
    useradd -u 1000 -g 1000 -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R 1000:1000 /usr/share/opensearch

# install yq
COPY --chown=0:0 config/yq-setup.sh /tmp/
RUN /tmp/yq-setup.sh

# Change User
USER 1000
WORKDIR /usr/share/opensearch

# Hard code node version and yarn version for now
# nvm environment variables
ENV NVM_DIR /usr/share/opensearch/.nvm
ENV NODE_VERSION 18.16.0
ENV CYPRESS_VERSION 12.13.0
ARG CYPRESS_VERSION_LIST="5.6.0 9.5.4 12.13.0"
ENV CYPRESS_LOCATION /usr/share/opensearch/.cache/Cypress/$CYPRESS_VERSION
ENV CYPRESS_LOCATION_954 /usr/share/opensearch/.cache/Cypress/9.5.4
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
COPY --chown=1000:1000 config/yarn-version.sh /tmp
RUN npm install -g yarn@`/tmp/yarn-version.sh main`
# Add legacy cypress@5.6.0 for 1.x line
# Add legacy cypress@9.5.4 for pre-2.8.0 releases
# Add latest cypress@12.13.0 for post-2.8.0 releases
RUN for cypress_version in $CYPRESS_VERSION_LIST; do npm install -g cypress@$cypress_version && npm cache verify; done

# Need root to get pass the build due to chrome sandbox needs to own by the root
USER 0

# Add legacy cypress 5.6.0 / 9.5.4 for ARM64 Architecture
RUN if [ `uname -m` = "aarch64" ]; then for cypress_version in 5.6.0 9.5.4; do rm -rf /usr/share/opensearch/.cache/Cypress/$cypress_version && \
    curl -SLO https://ci.opensearch.org/ci/dbc/tools/Cypress-$cypress_version-arm64.tar.gz && tar -xzf Cypress-$cypress_version-arm64.tar.gz -C /usr/share/opensearch/.cache/Cypress/ && \
    chown 1000:1000 -R /usr/share/opensearch/.cache/Cypress/$cypress_version && rm -vf Cypress-$cypress_version-arm64.tar.gz; done; fi

########################### Stage 1 ########################
FROM rockylinux:8

USER 0

# Add normal dependencies
RUN dnf clean all && dnf install -y 'dnf-command(config-manager)' && dnf config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo && \
    dnf update -y && \
    dnf install -y which curl git gnupg2 tar net-tools procps-ng python3 python3-devel python3-pip zip unzip gh

# Create user group
RUN groupadd -g 1000 opensearch && \
    useradd -u 1000 -g 1000 -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R 1000:1000 /usr/share/opensearch

# Copy from Stage0
COPY --from=linux_stage_0 --chown=1000:1000 /usr/share/opensearch /usr/share/opensearch
ENV NVM_DIR /usr/share/opensearch/.nvm
ENV NODE_VERSION 18.16.0
ENV CYPRESS_VERSION 12.13.0
ENV CYPRESS_LOCATION /usr/share/opensearch/.cache/Cypress/$CYPRESS_VERSION
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# Check dirs
RUN source $NVM_DIR/nvm.sh && ls -al /usr/share/opensearch && echo $NODE_VERSION $NVM_DIR && nvm use $NODE_VERSION

# Add Python37 dependencies
RUN yum install -y @development zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel findutils

# Add Dashboards dependencies (mainly for cypress)
RUN yum install -y xorg-x11-server-Xvfb gtk2-devel gtk3-devel libnotify-devel GConf2 nss libXScrnSaver alsa-lib

# Add Reports dependencies
RUN yum install -y nss xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-utils xorg-x11-fonts-cyrillic xorg-x11-fonts-Type1 xorg-x11-fonts-misc fontconfig freetype

# Add Yarn dependencies
RUN yum groupinstall -y "Development Tools" && yum clean all && rm -rf /var/cache/yum/*

# Setup Shared Memory
RUN chmod -R 777 /dev/shm

# Install Python37 binary
RUN curl https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz | tar xzvf - && \
    cd Python-3.7.7 && \
    ./configure --enable-optimizations && \
    make altinstall

# Setup Python37 links
RUN ln -sfn /usr/local/bin/python3.7 /usr/bin/python3 && \
    ln -sfn /usr/local/bin/pip3.7 /usr/bin/pip && \
    ln -sfn /usr/local/bin/pip3.7 /usr/local/bin/pip && \
    ln -sfn /usr/local/bin/pip3.7 /usr/bin/pip3

# Add other dependencies
RUN yum install -y epel-release && yum clean all && yum install -y chromium jq && yum clean all && rm -rf /var/cache/yum/* && \
    pip3 install pip==21.3.1 && \
    pip3 install cmake==3.21.3 && \
    pip3 install awscli==1.22.12 && \
    pip3 install pipenv

# Change User
USER 1000
WORKDIR /usr/share/opensearch

# We use the version test to check if packages installed correctly
# And get added to the PATH
# This will fail the docker build if any of the packages not exist
RUN node -v
RUN npm -v
RUN yarn -v
RUN cypress -v
