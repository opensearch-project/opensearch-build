#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.
#
# Modifications Copyright OpenSearch Contributors. See
# GitHub history for details.
# Copyright 2021 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# or in the "license" file accompanying this file. This file is distributed
# on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
# express or implied. See the License for the specific language governing
# permissions and limitations under the License.
#
# About:        This shell script generate an opensearch tarball with all the provided plugins installed and ready to use. 
#               A manifest file and right permissions set up is essential to download the required artifacts
# Dependencies: yq (More info: https://github.com/mikefarah/yq/tree/v4.4.1#install)
# Usage: .      /opensearch-tar-build.sh -f <path/to/manifest/file/>
#

set -e

function usage() {
    echo "Usage: $0 [args]"
    echo ""
    echo "Required arguments:"
    echo -e "-f MANIFEST_FILE\tPath/to/manifest.yml file"
    echo ""
    echo "Optional arguments:"
    echo -e "-p PLATFORM\tSpecify the platform. eg: linux, macos, windows. Currently only supports and defaults to linux"
    echo -e "-a ARCHITECTURE\tSpecify the architecture, e.g. x64, arm64. Currently only supports x64 and arm64. Defaults to x64"
    echo -e "-h help"
}

while getopts ":ha:p:f:" arg; do
    case $arg in
        h)
            usage
            exit 1
            ;;
        p)
            PLATFORM=$(echo "$OPTARG" | tr '[:upper:]' '[:lower:]')
            ;;
        a)
            ARCHITECTURE=$(echo "$OPTARG" | tr '[:upper:]' '[:lower:]')
            ;;
        f)
            MANIFEST_FILE=$OPTARG
            ;;
        :)
            echo "Error: -${OPTARG} requires an argument"
            usage
            exit 1
            ;;
        ?)
            echo "Invalid option: -${arg}"
            exit 1
            ;;
    esac
done

if [ -z "$PLATFORM" ]; then
    PLATFORM="linux"
fi

if [ -z "$ARCHITECTURE" ]; then
    ARCHITECTURE="x64"
fi

if [ -z "$MANIFEST_FILE" ]; then
    echo "Please specify the right path to manifest file"
    usage
    exit 1
fi
REPO_ROOT=`git rev-parse --show-toplevel`
VERSION=`yq eval '.version' $MANIFEST_FILE`
WORKING_DIR="opensearch-working-directory"
OPENSEARCH_CORE_URL=`yq eval '.products.opensearch.opensearch-min' $MANIFEST_FILE | sed s/^-// | sed -e 's/^[[:space:]]*//'`
OPENSEARCH_PLUGINS_URLS=`yq eval '.products.opensearch.plugins' $MANIFEST_FILE | sed s/^-// | sed -e 's/^[[:space:]]*//'`
LIBS=`yq eval '.products.opensearch.libs' $MANIFEST_FILE | sed s/^-// | sed -e 's/^[[:space:]]*//'`

# Download plugins to local 
mkdir -p ${WORKING_DIR}/plugins_downloads
IFS=$'\n'
cd ${WORKING_DIR}/plugins_downloads
for plugin in ${OPENSEARCH_PLUGINS_URLS}; do
  aws s3 cp $plugin . --profile staging
done

# Download k-NN lib
aws s3 cp $LIBS . --profile staging
unzip opensearch-knnlib-*-$PLATFORM-$ARCHITECTURE.zip

cd ..

# Download OpenSearch core TAR
wget -q ${OPENSEARCH_CORE_URL}
tar -xzf opensearch-min-*
rm *tar.gz

# Install plugins to OpenSearch
cd opensearch-*
for plugins in $OPENSEARCH_PLUGINS_URLS; do
    plugin=`basename $plugins`
  ./bin/opensearch-plugin install --batch file:../plugins_downloads/$plugin
done

echo "Plugins installed are:\n"
ls -tlr plugins

# Setup PA
cp -r plugins/opensearch-performance-analyzer/performance-analyzer-rca .
chmod -R 755 performance-analyzer-rca
mv bin/opensearch-performance-analyzer/performance-analyzer-agent-cli ./bin
ls -ltr ./bin
rm -rf ./bin/opensearch-performance-analyzer


# Make sure the data folder exists and is writable
if [ ! -d "data" ]; then 
    mkdir data
fi
chmod 755 data/

# Copy the tarball installation script 
cp $REPO_ROOT/release/tar/linux/opensearch-tar-install.sh .

# Setup k-NN-library
mkdir -p plugins/opensearch-knn/knnlib
cp ../plugins_downloads/opensearch-knnlib-*/libKNNIndexV2_0_11.so plugins/opensearch-knn/knnlib 


# Create TAR and Upload TAR to S3
cd ..
tar -czf opensearch-$VERSION-$PLATFORM-$ARCHITECTURE.tar.gz opensearch-*
cd ..
cp ${WORKING_DIR}/opensearch-$VERSION-$PLATFORM-$ARCHITECTURE.tar.gz .
rm -rf ${WORKING_DIR}