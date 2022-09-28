# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for standardize the ci/cd environment
# for both developers and ci/cd pipeline for releasing Opensearch clients and other products
# Please read the README.md file for all the information before using this dockerfile


FROM centos:7

ARG MAVEN_DIR=/usr/local/apache-maven

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

# Add Python37 dependencies
RUN yum install -y @development zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel findutils

# Add Yarn dependencies
RUN yum groupinstall -y "Development Tools" && yum clean all && rm -rf /var/cache/yum/*

# Tools setup
COPY --chown=0:0 config/jdk-setup.sh config/yq-setup.sh /tmp
RUN /tmp/jdk-setup.sh && /tmp/yq-setup.sh 

# Install higher version of maven 3.8.x
RUN export MAVEN_URL=`curl -s https://maven.apache.org/download.cgi | grep -Eo '["\047].*.bin.tar.gz["\047]' | tr -d '"'`  && \
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