# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for standardize the ci/cd environment
# for both developers and ci/cd pipeline for releasing Opensearch clients and other products
# Please read the README.md file for all the information before using this dockerfile

# Related dockerhub image: opensearchstaging/ci-runner:release-almalinux8-clients-v*


FROM almalinux:8

ARG MAVEN_DIR=/usr/local/apache-maven
ARG CONTAINER_USER=ci-runner
ARG CONTAINER_USER_HOME=/home/ci-runner

# Ensure localedef running correct with root permission
USER 0

# Add normal dependencies
RUN dnf clean all && \
    dnf update -y && \
    dnf install -y which curl git gnupg2 tar net-tools procps-ng python39 python39-devel python39-pip zip unzip jq

# Add Python dependencies
RUN dnf install -y @development zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel findutils

# Add Yarn dependencies
RUN dnf groupinstall -y "Development Tools" && dnf clean all && rm -rf /var/cache/dnf/*

# Installing dotnet
ARG DOT_NET_LIST="8.0"
RUN for dotnet_version in $DOT_NET_LIST; do dnf install -y dotnet-sdk-$dotnet_version; done

# Tools setup
COPY --chown=0:0 config/jdk-setup.sh config/yq-setup.sh config/gh-setup.sh /tmp/
RUN dnf install -y go && /tmp/jdk-setup.sh && /tmp/yq-setup.sh && /tmp/gh-setup.sh

# Create user group
RUN groupadd -g 1000 $CONTAINER_USER && \
    useradd -u 1000 -g 1000 -d $CONTAINER_USER_HOME $CONTAINER_USER && \
    mkdir -p $CONTAINER_USER_HOME && \
    chown -R 1000:1000 $CONTAINER_USER_HOME

# ENV JDK
ENV JAVA_HOME=/opt/java/openjdk-11
ENV PATH=$PATH:$JAVA_HOME/bin

# Installing higher version of maven 3.8.x
RUN export MAVEN_URL=`curl -s https://maven.apache.org/download.cgi | grep -Eo '["\047].*.bin.tar.gz["\047]' | tr -d '"' | uniq | head -n 1`  && \
    mkdir -p $MAVEN_DIR && (curl -s $MAVEN_URL | tar xzf - --strip-components=1 -C $MAVEN_DIR) && \
    echo "export M2_HOME=$MAVEN_DIR" > /etc/profile.d/maven_path.sh && \
    echo "export M2=\$M2_HOME/bin" >> /etc/profile.d/maven_path.sh && \
    echo "export PATH=\$M2:\$PATH" >> /etc/profile.d/maven_path.sh && \
    ln -sfn $MAVEN_DIR/bin/mvn /usr/local/bin/mvn

# Setup Shared Memory
RUN chmod -R 777 /dev/shm

# Setup Python
RUN update-alternatives --set python /usr/bin/python3.9 && \
    update-alternatives --set python3 /usr/bin/python3.9 && \
    pip3 install pip==23.1.2 && \
    pip3 install twine==4.0.2 cmake==3.26.4 pipenv==2023.6.12 awscli==1.32.17

# Installing osslsigncode
RUN dnf install -y libcurl-devel && dnf clean all && \
    mkdir -p /tmp/osslsigncode && cd /tmp/osslsigncode && \
    curl -sSL -o- https://github.com/mtrojnar/osslsigncode/archive/refs/tags/2.5.tar.gz  | tar -xz --strip-components 1 && \
    mkdir -p build && cd build && \
    cmake -S .. && cmake --build . && cmake --install . && \
    osslsigncode --version

# Installing rvm dependencies
RUN dnf install -y patch make ruby && dnf clean all

# Change User
USER $CONTAINER_USER
WORKDIR $CONTAINER_USER_HOME

# Install PKG builder dependencies with rvm
RUN curl -sSL https://rvm.io/mpapis.asc | gpg2 --import - && \
    curl -sSL https://rvm.io/pkuczynski.asc | gpg2 --import - && \
    curl -sSL https://get.rvm.io | bash -s stable

# Switch shell for rvm related commands
SHELL ["/bin/bash", "-lc"]
CMD ["/bin/bash", "-l"]

# Install ruby versions
RUN . $CONTAINER_USER_HOME/.rvm/scripts/rvm && \
    rvm install 2.6.0 && \
    rvm install 3.1.2 && \
    rvm install jruby-9.3.0.0 && \
    rvm --default use 2.6.0

ENV RVM_HOME=$CONTAINER_USER_HOME/.rvm/bin
ENV GEM_HOME=$CONTAINER_USER_HOME/.gem
ENV GEM_PATH=$GEM_HOME
ENV PATH=$RVM_HOME:$PATH

# Installing rust cargo
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y

ENV CARGO_PATH=$CONTAINER_USER_HOME/.cargo/bin
ENV PATH=$CARGO_PATH:$PATH

# nvm environment variables
ENV NVM_DIR $CONTAINER_USER_HOME/.nvm
ENV NODE_VERSION 16.20.0
ARG NODE_VERSION_LIST="10.24.1 14.19.1 14.20.0 14.20.1 14.21.3 16.20.0"

# Installing nvm
# https://github.com/creationix/nvm#install-script
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
# Installing node and npm
COPY --chown=$CONTAINER_USER:$CONTAINER_USER config/yarn-version.sh /tmp
RUN source $NVM_DIR/nvm.sh && \
    for node_version in $NODE_VERSION_LIST; do nvm install $node_version; npm install -g yarn@`/tmp/yarn-version.sh main`; done
# Add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH
# We use the version test to check if packages installed correctly
# And get added to the PATH
# This will fail the docker build if any of the packages not exist
RUN node -v
RUN npm -v
RUN yarn -v
RUN openssl version
RUN osslsigncode --version
RUN dotnet --version
RUN cargo --version
