# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for standardize the ci/cd environment
# for both developers and ci/cd pipeline for releasing Opensearch clients and other products
# Please read the README.md file for all the information before using this dockerfile

# Related dockerhub image: opensearchstaging/ci-runner:release-centos7-clients-v*


FROM centos:7

ARG MAVEN_DIR=/usr/local/apache-maven

# Ensure localedef running correct with root permission
USER 0

# Add normal dependencies
RUN yum clean all && yum-config-manager --add-repo https://cli.github.com/packages/rpm/gh-cli.repo && \
    yum update -y && \
    yum install -y which curl git gnupg2 tar net-tools procps-ng python3 python3-devel python3-pip zip unzip jq gh epel-release

# Add Python dependencies
RUN yum install -y @development zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel findutils

# Add Yarn dependencies
RUN yum groupinstall -y "Development Tools" && yum clean all && rm -rf /var/cache/yum/*

# Installing dotnet
ARG DOT_NET_LIST="6.0"
RUN rpm -Uvh https://packages.microsoft.com/config/centos/7/packages-microsoft-prod.rpm && \
    for dotnet_version in $DOT_NET_LIST; do yum install -y dotnet-sdk-$dotnet_version; done

RUN if [[ `uname -m` = 'aarch64' ]]; then mkdir -p aarch64-builds && cd aarch64-builds && \
    echo "Installing higher version of libstdc++ from Anaconda" && \
    curl -SL https://repo.anaconda.com/pkgs/main/linux-aarch64/libstdcxx-devel_linux-aarch64-11.2.0-h1234567_1.tar.bz2 -o libstdxxx-devel.tar.br2 && \
    tar --strip-components 2 -xjvf libstdxxx-devel.tar.br2 aarch64-conda-linux-gnu/lib64/libstdc++.so.6.0.29 && mv -v libstdc++.so.6.0.29 /lib64 && \
    ln -sfn /lib64/libstdc++.so.6.0.29 /lib64/libstdc++.so.6 && \
    echo "Installing glibc 2.18" && \
    curl -SLO https://ftp.gnu.org/gnu/glibc/glibc-2.18.tar.gz && tar -xzvf glibc-2.18.tar.gz && cd glibc-2.18 && mkdir -p build && cd build && \
    ../configure --prefix=/usr && make && make install && cd ../../ && \
    echo "Installing libicu 53+" && \
    rpm -e --nodeps libicu && \
    curl -SLO https://github.com/unicode-org/icu/releases/download/release-53-2/icu4c-53_2-src.tgz && tar -xzvf icu4c-53_2-src.tgz && cd icu && \
    cd source && ./configure --prefix=/usr && make && make install && \
    cd ../../../ && rm -rf aarch64-builds; fi

ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/lib

# Tools setup
COPY --chown=0:0 config/jdk-setup.sh config/yq-setup.sh /tmp/
RUN /tmp/jdk-setup.sh && /tmp/yq-setup.sh

# Create user group
RUN groupadd -g 1000 opensearch && \
    useradd -u 1000 -g 1000 -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R 1000:1000 /usr/share/opensearch

# Installing higher version of maven 3.8.x
RUN export MAVEN_URL=`curl -s https://maven.apache.org/download.cgi | grep -Eo '["\047].*.bin.tar.gz["\047]' | tr -d '"'`  && \
    mkdir -p $MAVEN_DIR && (curl -s $MAVEN_URL | tar xzf - --strip-components=1 -C $MAVEN_DIR) && \
    echo "export M2_HOME=$MAVEN_DIR" > /etc/profile.d/maven_path.sh && \
    echo "export M2=\$M2_HOME/bin" >> /etc/profile.d/maven_path.sh && \
    echo "export PATH=\$M2:\$PATH" >> /etc/profile.d/maven_path.sh && \
    ln -sfn $MAVEN_DIR/bin/mvn /usr/local/bin/mvn

# Setup Shared Memory
RUN chmod -R 777 /dev/shm

# Installing Python binary
RUN curl https://www.python.org/ftp/python/3.9.7/Python-3.9.7.tgz | tar xzvf - && \
    cd Python-3.9.7 && \
    ./configure --enable-optimizations && \
    make altinstall

# Setup Python links
RUN ln -sfn /usr/local/bin/python3.9 /usr/bin/python3 && \
    ln -sfn /usr/local/bin/pip3.9 /usr/bin/pip && \
    ln -sfn /usr/local/bin/pip3.9 /usr/local/bin/pip && \
    ln -sfn /usr/local/bin/pip3.9 /usr/bin/pip3 && \
    pip3 install pip==23.1.2 && pip3 install pipenv==2023.6.12 awscli==1.22.12

# Installing pip packages
RUN pip3 install twine==4.0.2 cmake==3.24.1.1

# Installing openssl1.1.1
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib:/usr/local/lib64:/usr/lib
RUN yum install -y curl libcurl-devel libfaketime perl-core pcre-devel && yum remove -y openssl-devel && yum clean all && \
    mkdir -p /tmp/openssl && cd /tmp/openssl && \
    curl -sSL -o- https://www.openssl.org/source/openssl-1.1.1g.tar.gz | tar -xz --strip-components 1 && \
    ./config --prefix=/usr --openssldir=/etc/ssl --libdir=lib shared zlib-dynamic && make && make install && \
    echo "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/lib:/usr/local/lib64:/usr/lib" > /etc/profile.d/openssl.sh && openssl version

# Installing osslsigncode
RUN mkdir -p /tmp/osslsigncode && cd /tmp/osslsigncode && source /etc/profile.d/openssl.sh && \
    curl -sSL -o- https://github.com/mtrojnar/osslsigncode/archive/refs/tags/2.5.tar.gz  | tar -xz --strip-components 1 && \
    mkdir -p build && cd build && cmake -S .. && cmake --build . && cmake --install . && osslsigncode --version

# Installing rvm dependencies
RUN yum install -y patch make ruby openssl-devel && yum clean all

# Change User
USER 1000
WORKDIR /usr/share/opensearch

# Installing PKG builder dependencies with rvm
RUN curl -sSL https://rvm.io/mpapis.asc | gpg2 --import - && \
    curl -sSL https://rvm.io/pkuczynski.asc | gpg2 --import - && \
    curl -sSL https://get.rvm.io | bash -s stable

# Switch shell for rvm related commands
SHELL ["/bin/bash", "-lc"]
CMD ["/bin/bash", "-l"]

# Installing rust cargo
RUN curl https://sh.rustup.rs -sSf | bash -s -- -y

# Installing ruby related dependencies
# Need to run either `. /usr/share/opensearch/.rvm/scripts/rvm` or `source /usr/share/opensearch/.rvm/scripts/rvm` 
# and force bash if needed before using the rvm command for any activities, or rvm will not correctly use version
RUN . /usr/share/opensearch/.rvm/scripts/rvm && rvm install 2.6.0 && rvm --default use 2.6.0 && \
    rvm install jruby-9.3.0.0

ENV RUBY_HOME=/usr/share/opensearch/.rvm/rubies/ruby-2.6.0/bin
ENV RVM_HOME=/usr/share/opensearch/.rvm/bin
ENV GEM_HOME=/usr/share/opensearch/.gem
ENV GEM_PATH=$GEM_HOME
ENV CARGO_PATH=/usr/share/opensearch/.cargo/bin
ENV PATH=$RUBY_HOME:$RVM_HOME:$CARGO_PATH:$PATH

# nvm environment variables
ENV NVM_DIR /usr/share/opensearch/.nvm
ENV NODE_VERSION 16.20.0
ARG NODE_VERSION_LIST="10.24.1 14.19.1 14.20.0 14.20.1 14.21.3 16.20.0"

# Installing nvm
# https://github.com/creationix/nvm#install-script
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
# Installing node and npm
COPY --chown=1000:1000 config/yarn-version.sh /tmp
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
