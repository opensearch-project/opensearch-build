# Copyright OpenSearch Contributors
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

# 20230920: On Docker host with systemd version > 247 you need to use these args:
# https://github.com/opensearch-project/opensearch-build/issues/4047
# --entrypoint=/usr/lib/systemd/systemd -u root --privileged -v /sys/fs/cgroup:/sys/fs/cgroup:rw --cgroupns=host

########################### Stage 0 ########################

FROM ubuntu:24.04 AS linux_stage_0

ENV container docker
ARG CONTAINER_USER=ci-runner
ARG CONTAINER_USER_HOME=/home/ci-runner

# Remove ubuntu user which occupies the 1000 userid and groupid since 23.04
# https://bugs.launchpad.net/cloud-images/+bug/2005129
USER 0
RUN touch /var/mail/ubuntu && chown ubuntu /var/mail/ubuntu && userdel -r ubuntu

SHELL ["/bin/bash", "-c"]

ARG DEBIAN_FRONTEND=noninteractive

# Install necessary packages
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y curl git gnupg2 tar procps build-essential cmake zip unzip jq && \
    apt-get install -y libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libnss3 libxss1 xauth xvfb && \
    apt-get install -y libxrender1 libxi6 libxtst6 libasound2t64 && \
    apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libatspi2.0-dev libxcomposite-dev libxdamage1 libxfixes3 libxfixes-dev libxrandr2 libgbm-dev libxkbcommon-x11-0 libpangocairo-1.0-0 libcairo2 libcairo2-dev libnss3 libnspr4 libnspr4-dev && \
    apt-get clean -y

# Install yq
COPY --chown=0:0 config/yq-setup.sh config/op-setup.sh /tmp/
RUN /tmp/yq-setup.sh && /tmp/op-setup.sh

# Create user group
RUN groupadd -g 1000 $CONTAINER_USER && \
    useradd -u 1000 -g 1000 -s /bin/bash -d $CONTAINER_USER_HOME -m $CONTAINER_USER && \
    mkdir -p $CONTAINER_USER_HOME && \
    chown -R 1000:1000 $CONTAINER_USER_HOME

# Change User
USER $CONTAINER_USER
WORKDIR $CONTAINER_USER_HOME

# Hard code node version and yarn version for now
# nvm environment variables
ENV NVM_DIR $CONTAINER_USER_HOME/.nvm
ENV NODE_VERSION 20.18.3
ENV CYPRESS_VERSION 9.5.4
ARG CYPRESS_VERSION_LIST="5.6.0 9.5.4"
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
# Add latest cypress@12.13.0 for post-2.8.0 releases, disable in 3.2.0 release due to install error https://github.com/cypress-io/cypress/issues/4595
RUN for cypress_version in $CYPRESS_VERSION_LIST; do npm install -g cypress@$cypress_version && npm cache verify; done

# Need root to get pass the build due to chrome sandbox needs to own by the root
USER 0

# Add legacy cypress 5.6.0 / 9.5.4 for ARM64 Architecture
RUN if [ `uname -m` = "aarch64" ]; then for cypress_version in 5.6.0 9.5.4; do rm -rf $CONTAINER_USER_HOME/.cache/Cypress/$cypress_version && \
    curl -SLO https://ci.opensearch.org/ci/dbc/tools/Cypress-$cypress_version-arm64.tar.gz && tar -xzf Cypress-$cypress_version-arm64.tar.gz -C $CONTAINER_USER_HOME/.cache/Cypress/ && \
    chown $CONTAINER_USER:$CONTAINER_USER -R $CONTAINER_USER_HOME/.cache/Cypress/$cypress_version && rm -vf Cypress-$cypress_version-arm64.tar.gz; done; fi

########################### Stage 1 ########################
FROM ubuntu:24.04

ARG CONTAINER_USER=ci-runner
ARG CONTAINER_USER_HOME=/home/ci-runner

# Remove ubuntu user which occupies the 1000 userid and groupid since 23.04
# https://bugs.launchpad.net/cloud-images/+bug/2005129
USER 0
RUN touch /var/mail/ubuntu && chown ubuntu /var/mail/ubuntu && userdel -r ubuntu

SHELL ["/bin/bash", "-c"]

ARG DEBIAN_FRONTEND=noninteractive

# Install python dependencies
RUN apt-get update -y && apt-get install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa -y

# Install necessary packages
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y curl git gnupg2 tar procps build-essential cmake zip unzip jq && \
    apt-get install -y libgtk2.0-0 libgtk-3-0 libgbm-dev libnotify-dev libnss3 libxss1 xauth xvfb && \
    apt-get install -y libxrender1 libxi6 libxtst6 libasound2t64 && \
    apt-get install -y libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libatspi2.0-dev libxcomposite-dev libxdamage1 libxfixes3 libxfixes-dev libxrandr2 libgbm-dev libxkbcommon-x11-0 libpangocairo-1.0-0 libcairo2 libcairo2-dev libnss3 libnspr4 libnspr4-dev && \
    apt-get install -y mandoc less pigz && \
    apt-get clean -y

# Install python, update awscli to v2 due to lib conflicts on urllib3 v1 vs v2
RUN apt-get update -y && apt-get install -y python3.9-full python3.9-dev && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 100 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.9 100 && \
    update-alternatives --set python3 /usr/bin/python3.9 && \
    update-alternatives --set python /usr/bin/python3.9 && \
    curl -SL https://bootstrap.pypa.io/get-pip.py | python3 - && \
    pip3 install awscliv2==2.3.1 pipenv==2023.6.12 cmake==3.26.4 && \
    ln -s `which awsv2` /usr/local/bin/aws && aws --install

# Create user group
RUN apt-get install -y sudo && \
    groupadd -g 1000 $CONTAINER_USER && \
    useradd -u 1000 -g 1000 -s /bin/bash -d $CONTAINER_USER_HOME -m $CONTAINER_USER && \
    mkdir -p $CONTAINER_USER_HOME && \
    chown -R 1000:1000 $CONTAINER_USER_HOME && \
    groupadd -g 1001 opensearch && \
    useradd -u 1001 -g 1001 -s /bin/bash -d /home/opensearch -m opensearch && \
    groupadd -g 1002 opensearch-dashboards && \
    useradd -u 1002 -g 1002 -s /bin/bash -d /home/opensearch-dashboards -m opensearch-dashboards && \
    usermod -a -G opensearch $CONTAINER_USER && \
    usermod -a -G opensearch-dashboards $CONTAINER_USER && \
    usermod -a -G adm $CONTAINER_USER && \
    id && \
    echo "$CONTAINER_USER ALL=(root) NOPASSWD:`which systemctl`, `which env`, `which su`, `which usermod`, `which apt`, `which apt-get`, `which apt-key`, `which dpkg`, `which chmod`, `which kill`, `which curl`, `which tee`, `which rm`, /usr/share/opensearch/bin/opensearch-plugin, /usr/share/opensearch-dashboards/bin/opensearch-dashboards-plugin" >> /etc/sudoers.d/$CONTAINER_USER

# Copy from Stage0
COPY --from=linux_stage_0 --chown=$CONTAINER_USER:$CONTAINER_USER $CONTAINER_USER_HOME $CONTAINER_USER_HOME
ENV NVM_DIR $CONTAINER_USER_HOME/.nvm
ENV NODE_VERSION 20.18.3
ENV CYPRESS_VERSION 9.5.4
ENV CYPRESS_LOCATION $CONTAINER_USER_HOME/.cache/Cypress/$CYPRESS_VERSION
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

# By default, awscliv2 will run with docker fallbacks and requires individual user to run `aws --install` to install binaries
# https://pypi.org/project/awscliv2/
USER $CONTAINER_USER
RUN aws --install
USER 0

# Check dirs
RUN source $NVM_DIR/nvm.sh && ls -al $CONTAINER_USER_HOME && echo $NODE_VERSION $NVM_DIR && nvm use $NODE_VERSION

# Tools setup
COPY --chown=0:0 config/jdk-setup.sh config/yq-setup.sh config/gh-setup.sh config/op-setup.sh /tmp/
RUN apt-get install -y golang-1.22 && /tmp/jdk-setup.sh && /tmp/yq-setup.sh && /tmp/gh-setup.sh && /tmp/op-setup.sh && apt-get clean -y && apt-get autoremove -y

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
