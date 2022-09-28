#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This script is used to build cypress, especially arm64 version
# as there is no arm64 version when you `npm install cypress`.
# The installed version will be fixed to x64 version

# DO NOT ADD -e as there will be compilation failure for some packages, but cypress will be built later
set -x

CPU_NUM=`cat /proc/cpuinfo | grep processor | wc -l`

if [ "$CPU_NUM" -le 4 ]
then
    echo "You need a server with more than 4 CPU to succeed the build"
    exit 1
fi

cd /tmp
git clone https://github.com/cypress-io/cypress.git cypress
cd cypress
git checkout tags/v$1 -b build-branch-$1
yarn install
yarn binary-build --version "$1"
yarn binary-zip
mv -v cypress.zip /tmp/cypress-$1.zip
exit 0
