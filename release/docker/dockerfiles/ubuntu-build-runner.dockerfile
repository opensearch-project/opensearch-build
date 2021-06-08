FROM ubuntu:20.04
# replace shell with bash so we can source files
RUN rm /bin/sh && ln -s /bin/bash /bin/sh
# update the repository sources list
# and install dependencies
RUN apt-get update -y && \
    apt-get upgrade -y && \
    apt-get install -y openjdk-14-jdk && \
    apt-get install -y curl && \
    apt-get install python -y && \
    apt-get install git -y && \
    apt-get install net-tools -y

## Setup Limits
#RUN sysctl -w vm.max_map_count=262144 && \
#    ulimit -n 65535 && \
RUN  chmod -R 777 /dev/shm

# Create user group
RUN groupadd -g 1000 opensearch && \
    useradd -u 1000 -g 1000 -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R 1000:1000 /usr/share/opensearch

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
