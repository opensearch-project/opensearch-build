# Copyright OpenSearch Contributors
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
ARG CONTAINER_USER=ci-runner
ARG CONTAINER_USER_HOME=/home/ci-runner

# Ensure localedef running correct with root permission
USER 0

# Add normal dependencies
RUN yum clean all && \
    amazon-linux-extras install epel -y && \
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

# Installing openssl1.1.1
# Support requests >= 2.28.1 version
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib:/usr/local/lib64:/usr/lib
RUN yum install -y curl libcurl-devel libfaketime perl-core pcre-devel && yum remove -y openssl-devel && yum clean all && \
    mkdir -p /tmp/openssl && cd /tmp/openssl && \
    curl -sSL -o- https://www.openssl.org/source/openssl-1.1.1g.tar.gz | tar -xz --strip-components 1 && \
    ./config --prefix=/usr --openssldir=/etc/ssl --libdir=lib shared zlib-dynamic && make && make install && \
    echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib:/usr/local/lib64:/usr/lib" > /etc/profile.d/openssl.sh && openssl version

# Install Python binary
RUN curl https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz | tar xzvf - && \
    cd Python-3.9.7 && \
    env LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib:/usr/local/lib64:/usr/lib ./configure --enable-optimizations --with-openssl=/usr --prefix=/usr/local && \
    make altinstall && cd ../ && rm -rf Python-3.9.7.tgz Python-3.9.7 && \
    cp -v /etc/ssl/certs/ca-bundle.crt /etc/ssl/cert.pem

# Setup Python links
RUN ln -sfn /usr/local/bin/python3.9 /usr/bin/python3 && \
    ln -sfn /usr/local/bin/pip3.9 /usr/bin/pip && \
    ln -sfn /usr/local/bin/pip3.9 /usr/local/bin/pip && \
    ln -sfn /usr/local/bin/pip3.9 /usr/bin/pip3 && \
    pip3 install pip==23.1.2 && pip3 install pipenv==2023.6.12 awscli==1.32.17

# Upgrade gcc
RUN yum install -y gcc10* && \
    mv -v /usr/bin/gcc /usr/bin/gcc7-gcc && \
    mv -v /usr/bin/g++ /usr/bin/gcc7-g++ && \
    mv -v /usr/bin/gfortran /usr/bin/gcc7-gfortran && \
    update-alternatives --install /usr/bin/gcc gcc $(which gcc10-gcc) 1 && \
    update-alternatives --install /usr/bin/g++ g++ $(which gcc10-g++) 1 && \
    update-alternatives --install /usr/bin/gfortran gfortran $(which gcc10-gfortran) 1
ENV FC=gfortran
ENV CXX=g++

# Add k-NN Library dependencies
RUN yum repolist && yum install lapack -y
RUN git clone -b v0.3.27 --single-branch https://github.com/xianyi/OpenBLAS.git && \
    cd OpenBLAS && \
    if [ "$(uname -m)" = "x86_64" ]; then \
        echo "Machine is x86_64. Adding DYNAMIC_ARCH=1 to openblas make command."; \
        make USE_OPENMP=1 FC=gfortran DYNAMIC_ARCH=1; \
    else \
        make USE_OPENMP=1 FC=gfortran; \
    fi && \
    make PREFIX=/usr/local install
ENV LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"
RUN pip3 install cmake==3.26.4

# NodeJS Unofficial Builds
# https://github.com/opensearch-project/opensearch-build/issues/5178
# https://github.com/actions/runner/issues/2906
# https://github.com/actions/runner/issues/3475
# GitHub enforce nodejs 20 official build in runner 2.317.0 of their actions and CentOS7/AL2 would fail due to having older glibc versions
# Until https://github.com/actions/runner/pull/3128 is merged or AL2 is deprecated (2025/06) this is a quick fix with unofficial builds support glibc 2.17
# With changes done similar to this PR (https://github.com/opensearch-project/job-scheduler/pull/702) alongside the image here
# Only linux x64 is supported in unofficial build until https://github.com/nodejs/unofficial-builds/pull/91 is merged
RUN if [ `uname -m` = "x86_64" ]; then \
        curl -SL https://unofficial-builds.nodejs.org/download/release/v20.10.0/node-v20.10.0-linux-x64-glibc-217.tar.xz -o /node20.tar.xz; \
        mkdir /node_al2; \
        tar -xf /node20.tar.xz --strip-components 1 -C /node_al2; \
        rm -v /node20.tar.xz; \
    fi

# Change User
USER $CONTAINER_USER
WORKDIR $CONTAINER_USER_HOME

# Install fpm for opensearch dashboards core
RUN gem install dotenv -v 2.8.1 && gem install public_suffix -v 5.1.1 && gem install fpm -v 1.14.2
ENV PATH=$CONTAINER_USER_HOME/.gem/gems/fpm-1.14.2/bin:$PATH
RUN fpm -v
