# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for standardize the ci/cd environment
# for both developers and ci/cd tools in OpenSearch / OpenSearch-Dashboards
# Please read the README.md file for all the information before using this dockerfile


FROM amazonlinux:2

ARG MAVEN_DIR=/usr/local/apache-maven

# Add AdoptOpenJDK Repo
RUN echo -e "[AdoptOpenJDK]\nname=AdoptOpenJDK\nbaseurl=http://adoptopenjdk.jfrog.io/adoptopenjdk/rpm/centos/7/\$basearch\nenabled=1\ngpgcheck=1\ngpgkey=https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public" > /etc/yum.repos.d/adoptopenjdk.repo

# Add normal dependencies
RUN yum clean all && \
    yum update -y && \
    yum install -y adoptopenjdk-14-hotspot which curl python git gnupg2 tar net-tools procps-ng python3 python3-pip python3-devel && \
    ln -sfn `which pip3` /usr/bin/pip && pip3 install pipenv && pipenv --version 

# Create user group
RUN groupadd -g 1000 opensearch && \
    useradd -u 1000 -g 1000 -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R 1000:1000 /usr/share/opensearch

# Add Dashboards dependencies
RUN yum install -y xorg-x11-server-Xvfb gtk2-devel gtk3-devel libnotify-devel GConf2 nss libXScrnSaver alsa-lib

# Add Notebook dependencies
RUN yum install -y libnss3.so xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-utils xorg-x11-fonts-cyrillic xorg-x11-fonts-Type1 xorg-x11-fonts-misc fontconfig freetype && yum clean all

# Add k-NN Library dependencies
RUN yum install epel-release -y && yum repolist && yum install openblas-static lapack -y
RUN pip3 install cmake==3.21.3

# Add Yarn dependencies
RUN yum groupinstall -y "Development Tools" && yum clean all && rm -rf /var/cache/yum/*

# Downloads JDK-8, JDK-11 and JDK-17 distributions using Eclipse Adoptium project.
# The distributions are extracted to /opt/java/ folder with environment variables JAVA8_HOME,
# JAVA11_HOME and JAVA17_HOME exported and pointing at respective ones.
RUN set -eux; \
    ARCH="$(uname -m)"; \
    JDKS=""; \
    case "${ARCH}" in \
       aarch64|arm64) \
         # Use "<checksum>@<URL>" format to collect all JDK platform specific distributions
         JDKS+="f287cdc2a688c2df247ea0d8bfe2863645b73848e4e5c35b02a8a3d2d6b69551@https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u302-b08/OpenJDK8U-jdk_aarch64_linux_hotspot_8u302b08.tar.gz "; \
         JDKS+="105bdc12fcd54c551e8e8ac96bc82412467244c32063689c41cee29ceb7452a2@https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.12%2B7/OpenJDK11U-jdk_aarch64_linux_hotspot_11.0.12_7.tar.gz "; \
         JDKS+="e08e6d8c84da28a2c49ccd511f8835c329fbdd8e4faff662c58fa24cca74021d@https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17%2B35/OpenJDK17-jdk_aarch64_linux_hotspot_17_35.tar.gz "; \
         ;; \
       amd64|x86_64) \
         # Use "<checksum>@<URL>" format to collect all JDK platform specific distributions
         JDKS+="cc13f274becf9dd5517b6be583632819dfd4dd81e524b5c1b4f406bdaf0e063a@https://github.com/adoptium/temurin8-binaries/releases/download/jdk8u302-b08/OpenJDK8U-jdk_x64_linux_hotspot_8u302b08.tar.gz "; \
         JDKS+="8770f600fc3b89bf331213c7aa21f8eedd9ca5d96036d1cd48cb2748a3dbefd2@https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.12%2B7/OpenJDK11U-jdk_x64_linux_hotspot_11.0.12_7.tar.gz "; \
         JDKS+="6f1335d9a7855159f982dac557420397be9aa85f3f7bc84e111d25871c02c0c7@https://github.com/adoptium/temurin17-binaries/releases/download/jdk-17%2B35/OpenJDK17-jdk_x64_linux_hotspot_17_35.tar.gz "; \
         ;; \
       *) \
         echo "Unsupported arch: ${ARCH}"; \
         exit 1; \
         ;; \
    esac; \
    for jdk in ${JDKS}; do \
        ESUM=$(echo ${jdk} | cut -d '@' -f1); \
        BINARY_URL=$(echo ${jdk} | cut -d '@' -f2); \
        regex="temurin([0-9]+)[-]"; \
        if [[ $jdk =~ $regex ]]; then \
            MAJOR=${BASH_REMATCH[1]}; \
            curl -LfsSo /tmp/openjdk-${MAJOR}.tar.gz ${BINARY_URL}; \
            echo "${ESUM} */tmp/openjdk-${MAJOR}.tar.gz" | sha256sum -c -; \
            mkdir -p /opt/java/openjdk-${MAJOR}; \
            cd /opt/java/openjdk-${MAJOR}; \
            tar -xf /tmp/openjdk-${MAJOR}.tar.gz --strip-components=1; \
            rm -rf /tmp/openjdk-${MAJOR}.tar.gz; \
            echo "export JAVA${MAJOR}_HOME=/opt/java/openjdk-${MAJOR}" >> /etc/profile.d/java_home.sh; \
        fi; \
    done;

# Install higher version of maven 3.8.x
RUN export MAVEN_URL=`curl -s https://maven.apache.org/download.cgi | grep -Eo '["\047].*.bin.tar.gz["\047]' | tr -d '"'`  && \
    mkdir -p $MAVEN_DIR && (curl -s $MAVEN_URL | tar xzf - --strip-components=1 -C $MAVEN_DIR) && \
    echo "export M2_HOME=$MAVEN_DIR" > /etc/profile.d/maven_path.sh && \
    echo "export M2=\$M2_HOME/bin" >> /etc/profile.d/maven_path.sh && \
    echo "export PATH=\$M2:\$PATH" >> /etc/profile.d/maven_path.sh && \
    ln -sfn $MAVEN_DIR/bin/mvn /usr/local/bin/mvn

# Setup Shared Memory
RUN chmod -R 777 /dev/shm

# Set JAVA_HOME and JAVA14_HOME
# AdoptOpenJDK apparently does not add JAVA_HOME after installation
RUN echo "export JAVA_HOME=`dirname $(dirname $(readlink -f $(which javac)))`" >> /etc/profile.d/java_home.sh && \
    echo "export JAVA14_HOME=`dirname $(dirname $(readlink -f $(which javac)))`" >> /etc/profile.d/java_home.sh

# Install PKG builder dependencies with rvm
RUN curl -sSL https://rvm.io/mpapis.asc | gpg2 --import - && \
    curl -sSL https://rvm.io/pkuczynski.asc | gpg2 --import - && \
    curl -sSL https://get.rvm.io | bash -s stable

# Switch shell for rvm related commands
SHELL ["/bin/bash", "-lc"]
CMD ["/bin/bash", "-l"]

# Install ruby / rpm / fpm related dependencies
RUN . /etc/profile.d/rvm.sh && rvm install 2.3.3 && rvm --default use 2.3.3 && \
    yum install -y rpm-build && \
    gem install fpm -v 1.13.0

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
RUN npm install -g cypress@^6.9.1 && npm cache verify
# We use the version test to check if packages installed correctly
# And get added to the PATH
# This will fail the docker build if any of the packages not exist
RUN node -v
RUN npm -v
RUN yarn -v
RUN cypress -v
