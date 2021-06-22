<<<<<<< HEAD
=======
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
#
# About: This docker file generates an image that can be used as standard build enviornment for building all artifacts
# Usage: docker build -f standard-build.dockerfile --tag <name>
# Build arguments:
#        UID: Optional. Specify the opensearch userid. Defaults to 1000.
#        GID: Optional. Specify the opensearch groupid. Defaults to 1000.

>>>>>>> d93fc077b7aefe90ccbe12fa39f16a5815678423
FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y openjdk-14-jdk && \
    apt-get install -y curl && \
    apt-get install python -y && \
    apt-get install git -y

ARG UID=1000
ARG GID=1000

# Create user and group
RUN groupadd -g $GID opensearch && \
    useradd -u $UID -g $GID -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R $UID:$GID /usr/share/opensearch


USER $UID

WORKDIR /usr/share/opensearch

# nvm environment variables
ENV NVM_DIR /usr/share/opensearch/.nvm
ENV NODE_VERSION 10.23.1

# install nvm
# https://github.com/creationix/nvm#install-script
RUN curl --silent -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.2/install.sh | bash

# install node and npm
RUN . $NVM_DIR/nvm.sh \
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