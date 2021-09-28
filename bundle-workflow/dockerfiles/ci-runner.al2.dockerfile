# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for standardize the ci/cd environment
# for both developers and ci/cd tools in OpenSearch / OpenSearch-Dashboards
# Please read the README.md file for all the information before using this dockerfile


FROM amazonlinux:2

# Add AdoptOpenJDK Repo
RUN echo -e "[AdoptOpenJDK]\nname=AdoptOpenJDK\nbaseurl=http://adoptopenjdk.jfrog.io/adoptopenjdk/rpm/centos/7/\$basearch\nenabled=1\ngpgcheck=1\ngpgkey=https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public" > /etc/yum.repos.d/adoptopenjdk.repo

# Add normal dependencies
RUN yum clean all && \
    yum update -y && \
    yum install -y adoptopenjdk-14-hotspot which curl python git tar net-tools procps-ng cmake python3 python3-pip python3-devel && \
    ln -sfn `which pip3` /usr/bin/pip && pip3 install pipenv && pipenv --version 

# Add Dashboards dependencies
RUN yum install -y xorg-x11-server-Xvfb gtk2-devel gtk3-devel libnotify-devel GConf2 nss libXScrnSaver alsa-lib

# Add Notebook dependencies
RUN yum install -y libnss3.so xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-utils xorg-x11-fonts-cyrillic xorg-x11-fonts-Type1 xorg-x11-fonts-misc fontconfig freetype && yum clean all

# Add Yarn dependencies
RUN yum groupinstall -y "Development Tools" && yum clean all && rm -rf /var/cache/yum/*

# Install higher version of maven 3.8.x
RUN (curl -s https://dlcdn.apache.org/maven/maven-3/3.8.2/binaries/apache-maven-3.8.2-bin.tar.gz | tar xzf - -C /usr/local/) && \
    echo "export M2_HOME=/usr/local/apache-maven-3.8.2" > /etc/profile.d/maven_path.sh && \
    echo "export M2=\$M2_HOME/bin" >> /etc/profile.d/maven_path.sh && \
    echo "export PATH=\$M2:\$PATH" >> /etc/profile.d/maven_path.sh && \
    ln -sfn /usr/local/apache-maven-3.8.2/bin/mvn /usr/local/bin/mvn

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
RUN npm install -g yarn@^1.21.1
# install cypress last known version that works for all existing opensearch-dashboards plugin integtests
RUN npm install -g cypress@^5.6.0 && npm cache verify
# We use the version test to check if packages installed correctly
# And get added to the PATH
# This will fail the docker build if any of the packages not exist
RUN node -v
RUN npm -v
RUN yarn -v
RUN cypress -v
