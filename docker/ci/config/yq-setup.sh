#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This script is to install yq properly on nix* server

set -ex

PLATFORM_LIST=(linux freebsd openbsd darwin)
for entry in ${PLATFORM_LIST[@]}; do
    if echo $OSTYPE | grep -o $entry; then
        PLATFORM=$entry
        break
    fi
done
ARCH=`uname -m`
VERSION="v4.27.2"

echo "$PLATFORM-$ARCH"

case $PLATFORM-$ARCH in
    linux-x86_64)
        YQ_TYPE="yq_linux_amd64"
        ;;
    linux-aarch64)
        YQ_TYPE="yq_linux_arm64"
        ;;
    freebsd-x86_64)
        YQ_TYPE="yq_freebsd_amd64"
        ;;
    openbsd-x86_64)
        YQ_TYPE="yq_openbsd_amd64"
        ;;
    darwin-x86_64)
        YQ_TYPE="yq_darwin_amd64"
        ;;
    darwin-arm64)
        YQ_TYPE="yq_darwin_arm64"
        ;;
    *)
        echo "Unsupported combination: $PLATFORM-$ARCH"
        exit 1
        ;;
esac

curl -SL https://github.com/mikefarah/yq/releases/download/$VERSION/$YQ_TYPE -o /usr/bin/yq
chmod 755 /usr/bin/yq
yq --version

echo "Installed yq"
