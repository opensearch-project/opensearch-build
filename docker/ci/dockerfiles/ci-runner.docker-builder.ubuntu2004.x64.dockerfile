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

FROM ubuntu:20.04

# Import necessary repository for installing qemu 5.0
RUN apt-get update -y && apt-get install -y software-properties-common && add-apt-repository ppa:jacob/virtualisation -y

# Install necessary packages
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y binfmt-support qemu qemu-user qemu-user-static docker.io curl python3-pip && apt clean -y && pip3 install awscli==1.22.12

# Install JDK
RUN curl -SL https://github.com/AdoptOpenJDK/openjdk14-binaries/releases/download/jdk-14.0.2%2B12/OpenJDK14U-jdk_x64_linux_hotspot_14.0.2_12.tar.gz -o /opt/jdk14.tar.gz && \
    mkdir -p /opt/java/openjdk-14 && \
    tar -xzf /opt/jdk14.tar.gz --strip-components 1 -C /opt/java/openjdk-14/ && \
    rm /opt/jdk14.tar.gz

# ENV JDK
ENV JAVA_HOME=/opt/java/openjdk-14
ENV PATH=$PATH:$JAVA_HOME/bin

# Install docker buildx
RUN mkdir -p ~/.docker/cli-plugins && \
    curl -SL https://github.com/docker/buildx/releases/download/v0.6.3/buildx-v0.6.3.linux-amd64 -o ~/.docker/cli-plugins/docker-buildx  && \
    chmod 775 ~/.docker/cli-plugins/docker-buildx && \
    docker buildx version


