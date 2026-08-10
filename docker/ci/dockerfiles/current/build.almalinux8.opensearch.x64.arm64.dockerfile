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

ARG MAVEN_DIR=/usr/local/apache-maven
ARG CONTAINER_USER=ci-runner
ARG CONTAINER_USER_HOME=/home/ci-runner

# Ensure localedef running correct with root permission
USER 0

# Add normal dependencies
# Install Python binary
# Install pip packages, including cmake for later k-NN usages
# ------
# Replace default curl 7.61.1 on Almalinux8 with 7.75+ version to support aws-sigv4
# https://github.com/curl/curl/commit/08e8455dddc5e48e58a12ade3815c01ae3da3b64
# https://curl.se/changes.html#7_75_0
# ------
# Install higher version of maven 3.8.x
# ------
# Add Python dependencies and Add Yarn dependencies
# Add Dashboards dependencies
# Add Notebook dependencies
# ------
# Create user group
RUN dnf clean all && dnf install -y 'dnf-command(config-manager)' && \
    dnf update -y && dnf install -y which curl git gnupg2 tar net-tools procps-ng python39 python39-devel python39-pip zip unzip jq pigz && \
    update-alternatives --set python /usr/bin/python3.9 && \
    update-alternatives --set python3 /usr/bin/python3.9 && \
    pip3 install pip==23.1.2 && pip3 install pipenv==2023.6.12 awscli==1.32.17 cmake==3.26.4 && \
    echo "------" && \
    ARCH=`uname -m`; \
    if [ "$ARCH" = "ppc64le" ]; then ARCH=powerpc64le; fi; \
    curl -SfL https://github.com/stunnel/static-curl/releases/download/8.6.0-1/curl-linux-$ARCH-8.6.0.tar.xz -o curl.tar.xz && \
    tar -xvf curl.tar.xz && mv -v curl /usr/local/bin/curl && rm -v curl.tar.xz && cd /etc/ssl/certs && ln -s ca-bundle.crt ca-certificates.crt && \
    echo "------" && \
    export MAVEN_URL=`curl -s https://maven.apache.org/download.cgi | grep -Eo '["\047].*.bin.tar.gz["\047]' | tr -d '"' | uniq | head -n 1`  && \
    mkdir -p $MAVEN_DIR && (curl -s $MAVEN_URL | tar xzf - --strip-components=1 -C $MAVEN_DIR) && \
    echo "export M2_HOME=$MAVEN_DIR" > /etc/profile.d/maven_path.sh && \
    echo "export M2=\$M2_HOME/bin" >> /etc/profile.d/maven_path.sh && \
    echo "export PATH=\$M2:\$PATH" >> /etc/profile.d/maven_path.sh && \
    ln -sfn $MAVEN_DIR/bin/mvn /usr/local/bin/mvn && \
    echo "------" && \
    dnf install -y @development zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel findutils && \
    dnf install -y xorg-x11-server-Xvfb gtk2-devel gtk3-devel libnotify-devel GConf2 nss libXScrnSaver alsa-lib && \
    dnf install -y nss xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-utils xorg-x11-fonts-cyrillic xorg-x11-fonts-Type1 xorg-x11-fonts-misc fontconfig freetype && \
    echo "------" && \
    groupadd -g 1000 $CONTAINER_USER && \
    useradd -u 1000 -g 1000 -d $CONTAINER_USER_HOME $CONTAINER_USER && \
    mkdir -p $CONTAINER_USER_HOME && \
    chown -R 1000:1000 $CONTAINER_USER_HOME

# Tools setup
# Setup Shared Memory
# ------
# Install PKG builder dependencies with rvm
COPY --chown=0:0 config/jdk-setup.sh config/yq-setup.sh config/gh-setup.sh config/op-setup.sh /tmp/
RUN dnf install -y go && /tmp/jdk-setup.sh && /tmp/yq-setup.sh && /tmp/gh-setup.sh && /tmp/op-setup.sh && \
    chmod -R 777 /dev/shm && \
    echo "------" && \
    curl -sSL https://rvm.io/mpapis.asc | gpg2 --import - && \
    curl -sSL https://rvm.io/pkuczynski.asc | gpg2 --import - && \
    curl -sSL https://get.rvm.io | bash -s stable

# Switch shell for rvm related commands
SHELL ["/bin/bash", "-lc"]
CMD ["/bin/bash", "-l"]

# Install ruby / rpm / fpm related dependencies
RUN . /etc/profile.d/rvm.sh && rvm install 2.6.0 && rvm --default use 2.6.0 && dnf install -y rpm-build rpm-sign createrepo pinentry
ENV RUBY_HOME=/usr/local/rvm/rubies/ruby-2.6.0/bin
ENV RVM_HOME=/usr/local/rvm/bin
ENV GEM_HOME=$CONTAINER_USER_HOME/.gem
ENV GEM_PATH=$GEM_HOME
ENV PATH=$RUBY_HOME:$RVM_HOME:$PATH

# Upgrade gcc (k-NN)
# The setup part is partially based on Austin Dewey's article:
# https://austindewey.com/2019/03/26/enabling-software-collections-binaries-on-a-docker-image/
RUN dnf install -y 'dnf-command(config-manager)' && \
    dnf config-manager --set-enabled powertools && \
    dnf install epel-release -y && dnf repolist && \
    dnf -y install gcc-toolset-13 && \
    echo "source /opt/rh/gcc-toolset-13/enable" > /etc/profile.d/gcc-toolset-13.sh
COPY --chown=0:0 config/gcc-toolset-13-setup /usr/local/bin/gcc_setup
ENV BASH_ENV="/usr/local/bin/gcc_setup"
ENV ENV="/usr/local/bin/gcc_setup"
ENV PROMPT_COMMAND=". /usr/local/bin/gcc_setup"

# Install openblas (k-NN)
ENV FC=gfortran
ENV CXX=g++
RUN yum repolist && yum install lapack -y && \
    git clone -b v0.3.27 --single-branch https://github.com/OpenMathLib/OpenBLAS.git && \
    cd OpenBLAS && \
    if [ "$(uname -m)" = "x86_64" ]; then \
        echo "Machine is x86_64. Adding DYNAMIC_ARCH=1 to openblas make command."; \
        make -j$(nproc) USE_OPENMP=1 FC=gfortran DYNAMIC_ARCH=1; \
    else \
        make -j$(nproc) USE_OPENMP=1 FC=gfortran; \
    fi && \
    make PREFIX=/usr/local install && \
    cd ../ && rm -rf OpenBLAS
ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"

# Change User
USER $CONTAINER_USER
WORKDIR $CONTAINER_USER_HOME

# Install Rust / protobuf
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- --default-toolchain stable -y && \
    if [ "$(uname -m)" = "x86_64" ]; then \
        curl -SfL https://github.com/protocolbuffers/protobuf/releases/download/v33.0/protoc-33.0-linux-x86_64.zip -o protoc.zip; \
    else \
        curl -SfL https://github.com/protocolbuffers/protobuf/releases/download/v33.0/protoc-33.0-linux-aarch_64.zip -o protoc.zip; \
    fi; \
    unzip protoc.zip -d $CONTAINER_USER_HOME/.local && rm -v protoc.zip

# Install fpm for opensearch dashboards core
RUN gem install dotenv -v 2.8.1 && gem install public_suffix -v 5.1.1 && gem install rchardet -v 1.8.0 && gem install fpm -v 1.14.2

# Setup ENV
ENV PATH=$CONTAINER_USER_HOME/.gem/gems/fpm-1.14.2/bin:$CONTAINER_USER_HOME/.local/bin:$PATH
RUN fpm -v && protoc --version
