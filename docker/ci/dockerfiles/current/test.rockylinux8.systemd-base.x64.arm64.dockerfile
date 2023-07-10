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
FROM rockylinux:8 AS linux_stage_0

ENV container docker

USER 0

# Add normal dependencies
RUN dnf clean all && \
    dnf update -y && \
    dnf install -y which curl git gnupg2 tar net-tools procps-ng python39 python39-devel python39-pip zip unzip jq

# Add Dashboards dependencies (mainly for cypress)
RUN dnf install -y xorg-x11-server-Xvfb gtk2-devel gtk3-devel libnotify-devel GConf2 nss libXScrnSaver alsa-lib

# Add Yarn dependencies
RUN dnf groupinstall -y "Development Tools" && dnf install -y cmake && dnf clean all

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
    dnf install -y which curl git gnupg2 tar net-tools procps-ng python39 python39-devel python39-pip zip unzip jq gh

# Create user group
RUN dnf install -y sudo && \
    groupadd -g 1000 opensearch && \
    useradd -u 1000 -g 1000 -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R 1000:1000 /usr/share/opensearch && \
    echo "opensearch ALL=(root) NOPASSWD:`which systemctl`, `which dnf`, `which yum`, `which rpm`, `which chmod`, `which kill`, `which curl`, /usr/share/opensearch-dashboards/bin/opensearch-dashboards-plugin" >> /etc/sudoers.d/opensearch

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

# Add Python dependencies
RUN dnf install -y @development zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel findutils

# Add Dashboards dependencies (mainly for cypress)
RUN dnf install -y xorg-x11-server-Xvfb gtk2-devel gtk3-devel libnotify-devel GConf2 nss libXScrnSaver alsa-lib

# Add Reports dependencies
RUN dnf install -y nss xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-utils xorg-x11-fonts-cyrillic xorg-x11-fonts-Type1 xorg-x11-fonts-misc fontconfig freetype

# Add Yarn dependencies
RUN dnf groupinstall -y "Development Tools" && dnf clean all

# Tools setup
COPY --chown=0:0 config/jdk-setup.sh config/yq-setup.sh /tmp/
RUN /tmp/jdk-setup.sh && /tmp/yq-setup.sh

# Setup Shared Memory
RUN chmod -R 777 /dev/shm

# Install Python binary
RUN update-alternatives --set python /usr/bin/python3.9 && \
    update-alternatives --set python3 /usr/bin/python3.9 && \
    pip3 install pip==23.1.2 && pip3 install pipenv==2023.6.12 awscli==1.22.12

# Add other dependencies
RUN dnf install -y epel-release && dnf clean all && dnf install -y chromium jq && dnf clean all && \
    pip3 install cmake==3.23.3

# We use the version test to check if packages installed correctly
# And get added to the PATH
# This will fail the docker build if any of the packages not exist
RUN node -v
RUN npm -v
RUN yarn -v
RUN cypress -v

# Possible retain of multi-user.target.wants later due to PA
# As of now we do not need this
RUN dnf -y install systemd procps util-linux-ng openssl openssl-devel which curl git gnupg2 tar net-tools jq && dnf clean all && \
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
