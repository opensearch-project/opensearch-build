# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for setting up systemd env base for services with root user
# It is initially designed to test pkg installation, but can be used for anything that requires systemd
# It used the method posted by Daniel Walsh: https://developers.redhat.com/blog/2014/05/05/running-systemd-within-docker-container

# In order to run images with systemd, you need to run in privileged mode: `docker run --privileged -it -v /sys/fs/cgroup:/sys/fs/cgroup:ro <image_tag>`
# If you use this image in jenkins pipeline you need to add these arguments: `args '--entrypoint=/usr/sbin/init -u root --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:ro'`

########################### Stage 0 ########################

FROM ubuntu:20.04 AS linux_stage_0

ENV container docker
SHELL ["/bin/bash", "-c"]

USER 0

ARG DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y curl git gnupg2 tar procps build-essential cmake zip unzip jq && \
    apt-get install -y libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2 libxtst6 xauth xvfb && \
    apt-get clean -y

# Install yq
COPY --chown=0:0 config/yq-setup.sh /tmp/
RUN /tmp/yq-setup.sh

# Create user group
RUN groupadd -g 1000 opensearch && \
    useradd -u 1000 -g 1000 -s /bin/bash -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R 1000:1000 /usr/share/opensearch 

# Change User
USER 1000
WORKDIR /usr/share/opensearch

# Hard code node version and yarn version for now
# nvm environment variables
ENV NVM_DIR /usr/share/opensearch/.nvm
ENV NODE_VERSION 16.14.2
ENV CYPRESS_VERSION 9.5.4
ENV CYPRESS_LOCATION /usr/share/opensearch/.cache/Cypress/$CYPRESS_VERSION
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
# install cypress last known version that works for all existing opensearch-dashboards plugin integtests
RUN npm install -g cypress@$CYPRESS_VERSION && npm cache verify
# Add legacy cypress@5.6.0 for 1.x line
RUN npm install -g cypress@5.6.0 && npm cache verify

# Need root to get pass the build due to chrome sandbox needs to own by the root
USER 0
# Build ARM64 Cypress
COPY --chown=0:0 config/cypress-setup.sh /tmp
RUN if [ `uname -m` = "aarch64" ]; then echo compile arm64 cypress && /tmp/cypress-setup.sh $CYPRESS_VERSION; fi
# replace default binary with arm64 specific binary from ci.opensearch.org
RUN if [ `uname -m` = "aarch64" ]; then rm -rf $CYPRESS_LOCATION/* && \
    unzip -q /tmp/cypress-$CYPRESS_VERSION.zip -d $CYPRESS_LOCATION/ && chown 1000:1000 -R $CYPRESS_LOCATION; fi && rm -rf /tmp/cypress*

# Add legacy cypress@5.6.0 for ARM64 Architecture
RUN if [ `uname -m` = "aarch64" ]; then rm -rf /usr/share/opensearch/.cache/Cypress/5.6.0 && \
    curl -SLO https://ci.opensearch.org/ci/dbc/tools/Cypress-5.6.0-arm64.tar.gz && tar -xzf Cypress-5.6.0-arm64.tar.gz -C /usr/share/opensearch/.cache/Cypress/ && \
    chown 1000:1000 -R /usr/share/opensearch/.cache/Cypress/5.6.0 && rm -vf Cypress-5.6.0-arm64.tar.gz; fi

########################### Stage 1 ########################
FROM ubuntu:20.04

SHELL ["/bin/bash", "-c"]

USER 0

ARG DEBIAN_FRONTEND=noninteractive

# Install python37 dependencies
RUN apt-get update -y && apt-get install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa -y

# Install python37 binaries
RUN apt-get update -y && apt-get install python3 && \
    apt-get install -y python3.7-full python3.7-dev && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.7 1 && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.7 1

# Install necessary packages
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y curl git gnupg2 tar procps build-essential cmake zip unzip jq && \
    apt-get install -y libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libgconf-2-4 libnss3 libxss1 libasound2 libxtst6 xauth xvfb && \
    apt-get install -y chromium-browser && \
    apt-get clean -y

# Install pip packages
RUN curl -SL https://bootstrap.pypa.io/get-pip.py | python && \
    pip3 install pip==21.3.1 && \
    pip3 install cmake==3.21.3 && \
    pip3 install awscli==1.22.12 && \
    pip3 install pipenv

# Create user group
RUN apt-get install -y sudo && \
    groupadd -g 1000 opensearch && \
    useradd -u 1000 -g 1000 -s /bin/bash -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R 1000:1000 /usr/share/opensearch && \
    echo "opensearch ALL=(root) NOPASSWD:`which systemctl`, `which apt`, `which apt-get`, `which apt-key`, `which dpkg`, `which chmod`, `which kill`, `which curl`, `which tee`" >> /etc/sudoers.d/opensearch

# Copy from Stage0
COPY --from=linux_stage_0 --chown=1000:1000 /usr/share/opensearch /usr/share/opensearch
ENV NVM_DIR /usr/share/opensearch/.nvm
ENV NODE_VERSION 16.14.2
ENV CYPRESS_VERSION 9.5.4
ENV CYPRESS_LOCATION /usr/share/opensearch/.cache/Cypress/$CYPRESS_VERSION
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# Check dirs
RUN source $NVM_DIR/nvm.sh && ls -al /usr/share/opensearch && echo $NODE_VERSION $NVM_DIR && nvm use $NODE_VERSION

# Tools setup
COPY --chown=0:0 config/jdk-setup.sh config/yq-setup.sh /tmp/
RUN /tmp/jdk-setup.sh && /tmp/yq-setup.sh

# Install gh cli
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=`dpkg --print-architecture` signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list && \
    apt-get update && apt-get install -y gh && apt-get clean

# Setup Shared Memory
RUN chmod -R 777 /dev/shm

# We use the version test to check if packages installed correctly
# And get added to the PATH
# This will fail the docker build if any of the packages not exist
RUN node -v
RUN npm -v
RUN yarn -v
RUN cypress -v

# Possible retain of multi-user.target.wants later due to PA
# As of now we do not need this
RUN apt-get -y install systemd procps util-linux openssl libssl-dev && apt-get clean -y && \
    systemctl set-default multi-user && \
(cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == systemd-tmpfiles-setup.service ] || rm -f $i; done); \
rm -f /lib/systemd/system/multi-user.target.wants/*;\
rm -f /etc/systemd/system/*.wants/*;\
rm -f /lib/systemd/system/local-fs.target.wants/*; \
rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
rm -f /lib/systemd/system/basic.target.wants/*;\
rm -f /lib/systemd/system/anaconda.target.wants/*;

CMD ["/usr/sbin/init"]
