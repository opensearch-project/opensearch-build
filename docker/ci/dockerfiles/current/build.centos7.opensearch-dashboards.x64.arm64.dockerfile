# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for standardize the ci/cd environment
# for both developers and ci/cd tools in OpenSearch / OpenSearch-Dashboards
# Please read the README.md file for all the information before using this dockerfile

# DOCKER_BUILD_SCRIPT_WITH_COMMANDS 
#  cd docker/ci && bash ./build-image-multi-arch.sh -v ci-runner-centos7-opensearch-dashboards-build -f dockerfiles/ci-runner.centos7.opensearch-dashboards.build.dockerfile

FROM centos:7

# Ensure localedef running correct with root permission
USER 0

# Setup ENV to prevent ASCII data issues with Python3
RUN echo "export LC_ALL=en_US.utf-8" >> /etc/profile.d/python3_ascii.sh && \
    echo "export LANG=en_US.utf-8" >> /etc/profile.d/python3_ascii.sh && \
    localedef -v -c -i en_US -f UTF-8 en_US.UTF-8 || echo set locale

# Add normal dependencies
RUN yum clean all && yum-config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo && \
    yum update -y && \
    yum install -y which curl git gnupg2 tar net-tools procps-ng python3 python3-devel python3-pip zip unzip jq gh

# Tools setup
COPY --chown=0:0 config/yq-setup.sh /tmp
RUN /tmp/yq-setup.sh

# Create user group
RUN groupadd -g 1000 opensearch && \
    useradd -u 1000 -g 1000 -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R 1000:1000 /usr/share/opensearch

# Add Python37 dependencies
RUN yum install -y @development zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel findutils

# Add Dashboards dependencies
RUN yum install -y xorg-x11-server-Xvfb gtk2-devel gtk3-devel libnotify-devel GConf2 nss libXScrnSaver alsa-lib

# Add Notebook dependencies
RUN yum install -y nss xorg-x11-fonts-100dpi xorg-x11-fonts-75dpi xorg-x11-utils xorg-x11-fonts-cyrillic xorg-x11-fonts-Type1 xorg-x11-fonts-misc fontconfig freetype && yum clean all

# Add Yarn dependencies
RUN yum groupinstall -y "Development Tools" && yum clean all && rm -rf /var/cache/yum/*

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
ENV GEM_HOME=/usr/share/opensearch/.gem
ENV GEM_PATH=$GEM_HOME
ENV PATH=$RUBY_HOME:$RVM_HOME:$PATH

# Install Python37 binary
RUN curl https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tgz | tar xzvf - && \
    cd Python-3.7.7 && \
    ./configure --enable-optimizations && \
    make altinstall

# Setup Python37 links
RUN ln -sfn /usr/local/bin/python3.7 /usr/bin/python3 && \
    ln -sfn /usr/local/bin/pip3.7 /usr/bin/pip && \
    ln -sfn /usr/local/bin/pip3.7 /usr/local/bin/pip && \
    ln -sfn /usr/local/bin/pip3.7 /usr/bin/pip3 && \
    pip3 install pipenv && pipenv --version

# Change User
USER 1000
WORKDIR /usr/share/opensearch

# Install fpm for opensearch dashboards core
RUN gem install fpm -v 1.14.2
ENV PATH=/usr/share/opensearch/.gem/gems/fpm-1.14.2/bin:$PATH

# Hard code node version and yarn version for now
# nvm environment variables
ENV NVM_DIR /usr/share/opensearch/.nvm
ENV NODE_VERSION 10.24.1
ARG NODE_VERSION_LIST="10.24.1 14.19.1 14.20.0"
COPY --chown=1000:1000 config/build-opensearch-dashboards-entrypoint.sh /usr/share/opensearch
# install nvm
# https://github.com/creationix/nvm#install-script
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
# install node and npm
RUN source $NVM_DIR/nvm.sh && \
    for node_version in $NODE_VERSION_LIST; do nvm install $node_version; npm install -g yarn@^1.21.1; done
# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH
# We use the version test to check if packages installed correctly
# And get added to the PATH
# This will fail the docker build if any of the packages not exist
RUN node -v
RUN npm -v
RUN yarn -v
RUN fpm -v
ENTRYPOINT ["bash", "/usr/share/opensearch/build-opensearch-dashboards-entrypoint.sh"]
CMD ["$NODE_VERSION"]
