# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This is a docker image specifically for building docker images with single/multi-arch support
# It has binfmt_support package installed to run non-native arch binary, as well as
# qemu-user-static package to enable execution of different multi-arch containers

# This can only be used on Ubuntu 2004 X64 version, as QEMU 5.0 is required to get buildx work properly without segfault
# https://bugs.launchpad.net/ubuntu/+source/qemu/+bug/1928075

# This image can be used with these arguments: -u root -v /var/run/docker.sock:/var/run/docker.sock

FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

# Import necessary repository for installing qemu 5.0
RUN apt-get update -y && apt-get install -y software-properties-common && add-apt-repository ppa:jacob/virtualisation -y

# Install necessary packages
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y binfmt-support qemu qemu-user qemu-user-static docker.io curl python3-pip && \
    apt-get install -y debmake debhelper-compat && \
    apt-get clean -y && pip3 install awscli==1.22.12

# Install gh cli
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg && \
    chmod go+r /usr/share/keyrings/githubcli-archive-keyring.gpg && \
    echo "deb [arch=`dpkg --print-architecture` signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | tee /etc/apt/sources.list.d/github-cli.list && \
    apt-get update && apt-get install -y gh && apt-get clean

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
RUN groupadd -g 1000 opensearch && \
    useradd -u 1000 -g 1000 -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R 1000:1000 /usr/share/opensearch 

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
