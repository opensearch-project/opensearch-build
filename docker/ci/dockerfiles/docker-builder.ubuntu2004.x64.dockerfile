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


# Create user group
RUN groupadd -g 1000 opensearch && \
    useradd -u 1000 -g 1000 -d /usr/share/opensearch opensearch && \
    mkdir -p /usr/share/opensearch && \
    chown -R 1000:1000 /usr/share/opensearch \
