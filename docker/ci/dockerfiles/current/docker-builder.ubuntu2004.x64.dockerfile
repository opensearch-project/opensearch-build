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

# Import necessary repository for installing qemu 5.0
RUN apt-get update -y && apt-get install -y software-properties-common && add-apt-repository ppa:jacob/virtualisation -y

# Install necessary packages
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y binfmt-support qemu qemu-user qemu-user-static docker.io curl python3-pip && apt clean -y && pip3 install awscli==1.22.12

# Install trivy to scan the docker images
RUN curl -SL https://github.com/aquasecurity/trivy/releases/download/v0.30.4/trivy_0.30.4_Linux-64bit.deb -o /tmp/trivy_0.30.4_Linux-64bit.deb && \
    dpkg -i /tmp/trivy_0.30.4_Linux-64bit.deb && rm /tmp/trivy_0.30.4_Linux-64bit.deb && \
    trivy --version

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
ENV JAVA_HOME=/opt/java/openjdk-11 \
    PATH=$PATH:$JAVA_HOME/bin

# Install docker buildx
RUN mkdir -p ~/.docker/cli-plugins && \
    curl -SL https://github.com/docker/buildx/releases/download/v0.6.3/buildx-v0.6.3.linux-amd64 -o ~/.docker/cli-plugins/docker-buildx  && \
    chmod 775 ~/.docker/cli-plugins/docker-buildx && \
    docker buildx version

# Install gcrane
RUN curl -L https://github.com/google/go-containerregistry/releases/latest/download/go-containerregistry_Linux_x86_64.tar.gz -o go-containerregistry.tar.gz && \
    tar -zxvf go-containerregistry.tar.gz && \
    chmod +x gcrane && \
    mv gcrane /usr/local/bin/ && \
    rm -rf go-containerregistry.tar.gz 
