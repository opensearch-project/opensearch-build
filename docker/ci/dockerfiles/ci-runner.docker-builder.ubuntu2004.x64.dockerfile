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
RUN apt-get update -y && apt-get upgrade -y && apt-get install -y binfmt-support qemu qemu-user qemu-user-static docker.io curl && apt clean -y

# Install docker buildx
RUN mkdir -p ~/.docker/cli-plugins && \
    curl -SL https://github.com/docker/buildx/releases/download/v0.6.3/buildx-v0.6.3.linux-amd64 -o ~/.docker/cli-plugins/docker-buildx  && \
    chmod 775 ~/.docker/cli-plugins/docker-buildx && \
    docker buildx version


