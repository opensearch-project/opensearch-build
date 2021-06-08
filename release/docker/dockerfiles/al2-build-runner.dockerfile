FROM amazonlinux:2
# replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh

# Add AdoptOpenJDK Repo
RUN echo -e "[AdoptOpenJDK]\nname=AdoptOpenJDK\nbaseurl=http://adoptopenjdk.jfrog.io/adoptopenjdk/rpm/centos/7/\$basearch\nenabled=1\ngpgcheck=1\ngpgkey=https://adoptopenjdk.jfrog.io/adoptopenjdk/api/gpg/key/public" > /etc/yum.repos.d/adoptopenjdk.repo

RUN yum update -y && \
    yum install -y adoptopenjdk-14-hotspot && \
    yum install -y curl && \
    yum install python -y && \
    yum install git -y && \
    yum install tar -y && \
    yum install net-tools -y && \
    yum install procps-ng -y && \
    yum clean all && \
    rm -rf /var/cache/yum/*

# Setup Shared Memory
RUN  chmod -R 777 /dev/shm

# Create user group
RUN groupadd -g 1000 opensearch && \
    useradd -u 1000 -g 1000 -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R 1000:1000 /usr/share/opensearch

# Change User
USER 1000
WORKDIR /usr/share/opensearch

# nvm environment variables
#ENV NVM_DIR $HOME/.nvm
ENV NVM_DIR /usr/share/opensearch/.nvm
ENV NODE_VERSION 10.23.1
# install nvm
# https://github.com/creationix/nvm#install-script
RUN curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.2/install.sh | bash
# install node and npm
RUN source $NVM_DIR/nvm.sh \
    && nvm install $NODE_VERSION \
    && nvm alias default $NODE_VERSION \
    && nvm use default
# add node and npm to path so the commands are available
ENV NODE_PATH $NVM_DIR/v$NODE_VERSION/lib/node_modules
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH
# install yarn
RUN npm install -g yarn@^1.22.1
# confirm installation
RUN node -v
RUN npm -v
RUN yarn -v
