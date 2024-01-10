#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This script is to install gh properly on nix* server

set -ex

PLATFORM_LIST=(linux)
for entry in "${PLATFORM_LIST[@]}"; do
    if echo $OSTYPE | grep -o $entry; then
        PLATFORM=$entry
        break
    fi
done
ARCH=`uname -m`
VERSION="2.42.0"

echo "$PLATFORM-$ARCH"

case $PLATFORM-$ARCH in
    linux-x86_64|linux-amd64)
        GH_TYPE="gh_${VERSION}_linux_amd64.tar.gz"
        ;;
    linux-aarch64|linux-arm64)
        GH_TYPE="gh_${VERSION}_linux_arm64.tar.gz"
        ;;
    linux-ppc64le)
        echo "ppc64le not supported by gh cli, skipping now so docker image creation can proceed"
        exit 0
        ;;
    *)
        echo "Unsupported combination: $PLATFORM-$ARCH"
        exit 1
        ;;
esac

curl -SL https://github.com/cli/cli/releases/download/v$VERSION/$GH_TYPE -o /tmp/$GH_TYPE
tar -xzf /tmp/$GH_TYPE --strip-component=1 -C /usr
rm -v /tmp/$GH_TYPE
chmod 755 /usr/bin/gh
gh --version

echo "Installed gh $VERSION"
