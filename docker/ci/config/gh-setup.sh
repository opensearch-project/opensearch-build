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

# ppc64le specific
function gh_install_ppc64le {
    set -e    
    GO_VERSION=`go version | cut -d ' ' -f3 | tr -d 'go'`
    GO_REQUIRED_VERSION="1.21.0"
    COMPARE_VERSION=`echo $GO_REQUIRED_VERSION $GO_VERSION | tr ' ' '\n' | sort -V | uniq | head -n 1`
    if [ "$COMPARE_VERSION" != "$GO_REQUIRED_VERSION" ]; then
        VERSION=2.32.1
        echo "go version on this env is older than $GO_REQUIRED_VERSION, use gh $VERSION"
    fi

    git clone --single-branch --branch v$VERSION https://github.com/cli/cli.git gh-cli
    cd gh-cli
    make install
    cd ../
    rm -rf gh-cli
    gh --version
}

echo "$PLATFORM-$ARCH"

case $PLATFORM-$ARCH in
    linux-x86_64|linux-amd64)
        GH_TYPE="gh_${VERSION}_linux_amd64.tar.gz"
        ;;
    linux-aarch64|linux-arm64)
        GH_TYPE="gh_${VERSION}_linux_arm64.tar.gz"
        ;;
    linux-ppc64le)
        gh_install_ppc64le
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
