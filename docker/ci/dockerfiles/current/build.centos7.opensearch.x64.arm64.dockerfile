# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for standardize the ci/cd environment
# for both developers and ci/cd tools in OpenSearch / OpenSearch-Dashboards
# Please read the README.md file for all the information before using this dockerfile


FROM centos:7

ARG MAVEN_DIR=/usr/local/apache-maven
ARG CONTAINER_USER=ci-runner
ARG CONTAINER_USER_HOME=/home/ci-runner

# Ensure localedef running correct with root permission
USER 0

# Add normal dependencies
RUN yum clean all && \
    yum install epel-release -y && \
    yum update -y && \
    yum install -y which curl git gnupg2 tar net-tools procps-ng python3 python3-devel python3-pip zip unzip jq pigz

# Create user group
RUN groupadd -g 1000 $CONTAINER_USER && \
    useradd -u 1000 -g 1000 -d $CONTAINER_USER_HOME $CONTAINER_USER && \
    mkdir -p $CONTAINER_USER_HOME && \
    chown -R 1000:1000 $CONTAINER_USER_HOME

# Add Python dependencies
RUN yum install -y @development zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel findutils

# Add Dashboards dependencies
RUN yum install -y xorg-x11-server-Xvfb gtk2-devel gtk3-devel libnotify-devel GConf2 nss libXScrnSaver alsa-lib

# Add Notebook dependencies
RUN yum install -y nss xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-utils xorg-x11-fonts-cyrillic xorg-x11-fonts-Type1 xorg-x11-fonts-misc fontconfig freetype && yum clean all

# Add Yarn dependencies
RUN yum groupinstall -y "Development Tools" && yum clean all && rm -rf /var/cache/yum/*

# Tools setup
COPY --chown=0:0 config/jdk-setup.sh config/yq-setup.sh config/gh-setup.sh /tmp/
RUN yum install -y go && /tmp/jdk-setup.sh && /tmp/yq-setup.sh && /tmp/gh-setup.sh

# Install higher version of maven 3.8.x
RUN export MAVEN_URL=`curl -s https://maven.apache.org/download.cgi | grep -Eo '["\047].*.bin.tar.gz["\047]' | tr -d '"' | uniq | head -n 1`  && \
    mkdir -p $MAVEN_DIR && (curl -s $MAVEN_URL | tar xzf - --strip-components=1 -C $MAVEN_DIR) && \
    echo "export M2_HOME=$MAVEN_DIR" > /etc/profile.d/maven_path.sh && \
    echo "export M2=\$M2_HOME/bin" >> /etc/profile.d/maven_path.sh && \
    echo "export PATH=\$M2:\$PATH" >> /etc/profile.d/maven_path.sh && \
    ln -sfn $MAVEN_DIR/bin/mvn /usr/local/bin/mvn

# Setup Shared Memory
RUN chmod -R 777 /dev/shm

# Install PKG builder dependencies with rvm
RUN curl -sSL https://rvm.io/mpapis.asc | gpg2 --import - && \
    curl -sSL https://rvm.io/pkuczynski.asc | gpg2 --import - && \
    curl -sSL https://get.rvm.io | bash -s stable

# Switch shell for rvm related commands
SHELL ["/bin/bash", "-lc"]
CMD ["/bin/bash", "-l"]

# Install ruby / rpm / fpm related dependencies
RUN . /etc/profile.d/rvm.sh && rvm install 2.6.0 && rvm --default use 2.6.0 && yum install -y rpm-build createrepo && yum clean all

ENV RUBY_HOME=/usr/local/rvm/rubies/ruby-2.6.0/bin
ENV RVM_HOME=/usr/local/rvm/bin
ENV GEM_HOME=$CONTAINER_USER_HOME/.gem
ENV GEM_PATH=$GEM_HOME
ENV PATH=$RUBY_HOME:$RVM_HOME:$PATH

# Install Python binary
RUN curl https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz | tar xzvf - && \
    cd Python-3.9.7 && \
    ./configure --enable-optimizations && \
    make altinstall

# Setup Python links
RUN ln -sfn /usr/local/bin/python3.9 /usr/bin/python3 && \
    ln -sfn /usr/local/bin/pip3.9 /usr/bin/pip && \
    ln -sfn /usr/local/bin/pip3.9 /usr/local/bin/pip && \
    ln -sfn /usr/local/bin/pip3.9 /usr/bin/pip3 && \
    pip3 install pip==23.1.2 && pip3 install pipenv==2023.6.12 awscli==1.32.17

# Add k-NN Library dependencies
RUN yum install epel-release -y && yum repolist && yum install openblas-static lapack gcc-gfortran -y
RUN pip3 install cmake==3.23.3
# Upgrade gcc
# The setup part is partially based on Austin Dewey's article:
# https://austindewey.com/2019/03/26/enabling-software-collections-binaries-on-a-docker-image/
RUN yum install -y centos-release-scl && yum install -y devtoolset-9 && yum clean all && \
    echo "source scl_source enable devtoolset-9" > /etc/profile.d/scl_devtoolset9.sh
COPY --chown=0:0 config/scl_setup_devtoolset9 /usr/local/bin/scl_setup
ENV BASH_ENV="/usr/local/bin/scl_setup"
ENV ENV="/usr/local/bin/scl_setup"
ENV PROMPT_COMMAND=". /usr/local/bin/scl_setup"

# Change User
USER $CONTAINER_USER
WORKDIR $CONTAINER_USER_HOME

# Install fpm for opensearch dashboards core
RUN gem install dotenv -v 2.8.1 && gem install fpm -v 1.14.2
ENV PATH=$CONTAINER_USER_HOME/.gem/gems/fpm-1.14.2/bin:$PATH
RUN fpm -v
