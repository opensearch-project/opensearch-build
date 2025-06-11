# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for building docker images with single/multi-arch support
# It has binfmt_support package installed to run non-native arch binary, as well as
# qemu-user-static package to enable execution of different multi-arch containers

# This can only be used on Ubuntu 2404 X64 version, as QEMU 8.2 is required to get buildx work properly without segfault
# A similar issue on Ubuntu 2004 with QEMU 5.0 requirements has been documented here:
# https://bugs.launchpad.net/ubuntu/+source/qemu/+bug/1928075

# This image can be used with these arguments: -u root -v /var/run/docker.sock:/var/run/docker.sock

FROM ubuntu:24.04

ARG DEBIAN_FRONTEND=noninteractive
ARG CONTAINER_USER=ci-runner
ARG CONTAINER_USER_HOME=/home/ci-runner

# Remove ubuntu user which occupies the 1000 userid and groupid since 23.04
# https://bugs.launchpad.net/cloud-images/+bug/2005129
USER 0
RUN touch /var/mail/ubuntu && chown ubuntu /var/mail/ubuntu && userdel -r ubuntu

# Import necessary repository
RUN apt-get update -y && apt-get install -y software-properties-common && add-apt-repository ppa:deadsnakes/ppa -y

# Install necessary packages to build multi-arch docker images
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y binfmt-support qemu-system qemu-system-common qemu-user qemu-user-static docker.io=24.0.7* curl && \
    apt-get install -y mandoc less && \
    apt-get install -y debmake debhelper-compat

# Install python, update awscli to v2 due to lib conflicts on urllib3 v1 vs v2
RUN apt-get install -y python3.9-full python3.9-dev && \
    update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 100 && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3.9 100 && \
    update-alternatives --set python3 /usr/bin/python3.9 && \
    update-alternatives --set python /usr/bin/python3.9 && \
    curl -SL https://bootstrap.pypa.io/get-pip.py | python3 - && \
    pip3 install awscliv2==2.3.1 && \
    ln -s `which awsv2` /usr/local/bin/aws && aws --install

# Install trivy to scan the docker images
RUN apt-get install -y apt-transport-https gnupg lsb-release && \
    curl -o- https://aquasecurity.github.io/trivy-repo/deb/public.key | gpg --dearmor | tee /usr/share/keyrings/trivy.gpg > /dev/null && \
    echo "deb [signed-by=/usr/share/keyrings/trivy.gpg] https://aquasecurity.github.io/trivy-repo/deb $(lsb_release -sc) main" | tee -a /etc/apt/sources.list.d/trivy.list && \
    apt-get update -y && apt-get install -y trivy && apt-get clean && trivy --version

# Install JDK
RUN curl -SL https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.15%2B10/OpenJDK11U-jdk_x64_linux_hotspot_11.0.15_10.tar.gz -o /opt/jdk11.tar.gz && \
    mkdir -p /opt/java/openjdk-11 && \
    tar -xzf /opt/jdk11.tar.gz --strip-components 1 -C /opt/java/openjdk-11/ && \
    rm /opt/jdk11.tar.gz

# Create user group
RUN groupadd -g 1000 $CONTAINER_USER && \
    useradd -u 1000 -g 1000 -s /bin/bash -d $CONTAINER_USER_HOME -m $CONTAINER_USER && \
    mkdir -p $CONTAINER_USER_HOME && \
    chown -R 1000:1000 $CONTAINER_USER_HOME

# By default, awscliv2 will run with docker fallbacks and requires individual user to run `aws --install` to install binaries
# https://pypi.org/project/awscliv2/
USER $CONTAINER_USER
RUN aws --install
USER 0

# ENV JDK
ENV JAVA_HOME=/opt/java/openjdk-11
ENV PATH=$PATH:$JAVA_HOME/bin

# Install docker buildx
# 2023-06-20 Upgrade from 0.6.3 to 0.9.1 due to binary translation speedup in emulation mode during multi-arch image generation
# https://github.com/docker/buildx/releases/tag/v0.9.1
# Avoid upgrading to 0.10.0+ due to this change:
#   Buildx v0.10 enables support for a minimal SLSA Provenance attestation, which requires support for OCI-compliant multi-platform images.
#   This may introduce issues with registry and runtime support (e.g. Google Cloud Run and Lambda).
#   You can optionally disable the default provenance attestation functionality using --provenance=false.
RUN mkdir -p ~/.docker/cli-plugins && \
    curl -SL https://github.com/docker/buildx/releases/download/v0.9.1/buildx-v0.9.1.linux-amd64 -o ~/.docker/cli-plugins/docker-buildx  && \
    chmod 775 ~/.docker/cli-plugins/docker-buildx && \
    docker buildx version

# Install gcrane
# Stays on 0.15.2 due to --all-tags was introduced in 0.15.1 and several bugs are fixed in 0.15.2: https://github.com/google/go-containerregistry/pull/1682
RUN curl -SL https://github.com/google/go-containerregistry/releases/download/v0.15.2/go-containerregistry_Linux_x86_64.tar.gz -o go-containerregistry.tar.gz && \
    tar -zxvf go-containerregistry.tar.gz && \
    chmod +x gcrane crane krane && \
    mv -v gcrane crane krane /usr/local/bin/ && \
    rm -v go-containerregistry.tar.gz && \
    gcrane version && crane version && krane version

# Install packer
# Stays on 1.8.7 version due to 1.8.7 fixed the JSON regression: https://github.com/hashicorp/packer/issues/12281
# As well as 1.9.0+ includes major changes. A lot of plugins are removed since 1.9.0: https://github.com/hashicorp/packer/releases/tag/v1.9.0
RUN curl -SL -o- https://apt.releases.hashicorp.com/gpg | gpg --dearmor > /usr/share/keyrings/hashicorp-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | tee /etc/apt/sources.list.d/hashicorp.list && \
    apt-get update && \
    apt-get install packer=1.8.7* && \
    packer --version && \
    apt-get clean

# Tools setup
COPY --chown=0:0 config/yq-setup.sh config/gh-setup.sh config/op-setup.sh /tmp/
RUN apt-get install -y golang-1.22 && /tmp/yq-setup.sh && /tmp/gh-setup.sh && /tmp/op-setup.sh && apt-get clean && apt-get autoremove -y
