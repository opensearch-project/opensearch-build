#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This script is to install onepassword-cli (op) properly on nix* server

set -ex

PLATFORM_LIST=(linux darwin)
for entry in ${PLATFORM_LIST[@]}; do
    if echo $OSTYPE | grep -o $entry; then
        PLATFORM=$entry
        break
    fi
done

ARCH=`uname -m`
VERSION="v2.31.1"

echo "$PLATFORM-$ARCH"

case $PLATFORM-$ARCH in
    linux-x86_64|linux-amd64)
        ARCH_FINAL="amd64"
        ;;
    linux-aarch64|linux-arm64)
        ARCH_FINAL="arm64"
        ;;
    linux-ppc64le)
        echo "PPC64LE is not supported at the moment"
        exit 0
        ;;
    darwin-x86_64|darwin-arm64)
        brew install 1password-cli
        exit 0
        ;;
    *)
        echo "Unsupported combination: $PLATFORM-$ARCH"
        exit 1
        ;;
esac

curl -SfL https://cache.agilebits.com/dist/1P/op2/pkg/${VERSION}/op_${PLATFORM}_${ARCH_FINAL}_${VERSION}.zip -o /tmp/op.zip
unzip -j /tmp/op.zip op -d /usr/local/bin
rm -v /tmp/op.zip
op --version

echo "Installed op"
