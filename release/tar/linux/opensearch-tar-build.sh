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
# About:        This shell script generate an opensearch tarball with all the provided plugins installed and ready to use. 
#               A manifest file and right permissions set up is essential to download the required artifacts
# Dependencies: yq (More info: https://github.com/mikefarah/yq/tree/v4.4.1#install)
# Usage:        ./opensearch-tar-build.sh -f <path/to/manifest/file/>
#

set -e

function usage() {
    echo "Usage: $0 [args]"
    echo -e "Supported manifest schema-version: 1.0"
    echo ""
    echo "Required arguments:"
    echo -e "-f MANIFEST_FILE\tPath/to/manifest.yml file"
    echo ""
    echo "Optional arguments:"
    echo -e "-h help"
}

while getopts ":ha:p:f:" arg; do
    case $arg in
        h)
            usage
            exit 1
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

if [ -z "$MANIFEST_FILE" ]; then
    echo "error: You must specify the manifest file"
    usage
    exit 1
fi

if [ ! -f "$MANIFEST_FILE" ]; then
    echo "error: The given file doesnot exist. Please check the specified path"
    usage
    exit 1
fi

SCHEMA_VERSION=`yq eval '.manifest.schema-version' $MANIFEST_FILE`
PLATFORM=`yq eval '.build.platform' $MANIFEST_FILE`
ARCHITECTURE=`yq eval '.build.architecture' $MANIFEST_FILE`
VERSION=`yq eval '.build.version' $MANIFEST_FILE`

if [ -z "$VERSION" ]; then
    echo "error: Please specify the version in the manifest file"
    usage
    exit 1
fi

if [ "$SCHEMA_VERSION" != "1.0" ]; then
    echo "error: This script only supports manifest schema version 1.0. Please use the manifest file with right schema version"
    usage
    exit 1
fi

if [ "$PLATFORM" != "linux" ]; then
    echo "error: $PLATFORM platform is not supported yet! Only supported platform is linux"
    usage
    exit 1
fi

if [ "$ARCHITECTURE" != "x64" ] && [ "$ARCHITECTURE" != "arm64" ]
then
    echo "error: $ARCHITECTURE architecture is not supported yet! Only supported architectures are x64 and arm64"
    usage
    exit 1
fi

REPO_ROOT=`git rev-parse --show-toplevel`
BASE_DIR="opensearch-working-directory"
TARGET_DIR=`pwd`
OPENSEARCH_CORE_URL=`yq eval '.products.opensearch.opensearch-min' $MANIFEST_FILE | sed s/^-// | sed -e 's/^[[:space:]]*//'`
OPENSEARCH_PLUGINS_URLS=`yq eval '.products.opensearch.plugins' $MANIFEST_FILE | sed s/^-// | sed -e 's/^[[:space:]]*//'`
LIBS=`yq eval '.products.opensearch.libs' $MANIFEST_FILE | sed s/^-// | sed -e 's/^[[:space:]]*//'`

# # Download plugins to local 
mkdir -p $BASE_DIR/plugins_downloads
cd $BASE_DIR
WORKING_DIR=`pwd`
echo "working dir is: ${WORKING_DIR}"
IFS=$'\n'
cd ${WORKING_DIR}/plugins_downloads
for plugin in ${OPENSEARCH_PLUGINS_URLS}; do
  aws s3 cp $plugin .
done

# # Download k-NN lib
aws s3 cp $LIBS .
unzip opensearch-knnlib-*-$PLATFORM-$ARCHITECTURE.zip

# Download OpenSearch core TAR
wget -q ${OPENSEARCH_CORE_URL} -O opensearch.tar.gz
tar -xzf opensearch.tar.gz --strip-components=1 --directory "$WORKING_DIR" && rm -rf opensearch.tar.gz

# Install plugins to OpenSearch
cd ${WORKING_DIR}
for plugins in $OPENSEARCH_PLUGINS_URLS; do
    plugin=`basename $plugins`
  ./bin/opensearch-plugin install --batch file:${WORKING_DIR}/plugins_downloads/$plugin
done

echo "Plugins installed are:"
ls -tlr plugins

# Setup Performance Analyzer Agent
cp -r plugins/opensearch-performance-analyzer/performance-analyzer-rca .
chmod -R 755 performance-analyzer-rca
mv bin/opensearch-performance-analyzer/performance-analyzer-agent-cli ./bin
rm -rf ./bin/opensearch-performance-analyzer

mkdir -p data
chmod 755 data/

# Copy the tarball installation script 
cp $REPO_ROOT/release/tar/linux/opensearch-tar-install.sh $WORKING_DIR/

# Setup k-NN-library
mkdir -p $WORKING_DIR/plugins/opensearch-knn/knnlib
cp $WORKING_DIR/plugins_downloads/opensearch-knnlib-*/libKNNIndexV2_0_11.so $WORKING_DIR/plugins/opensearch-knn/knnlib 

# Tar the bundle and clean up
rm -rf plugins_downloads
tar -czf $TARGET_DIR/opensearch-$VERSION-$PLATFORM-$ARCHITECTURE.tar.gz $TARGET_DIR/$BASE_DIR
cd $TARGET_DIR
shasum -a 512 opensearch-$VERSION-$PLATFORM-$ARCHITECTURE.tar.gz > opensearch-$VERSION-$PLATFORM-$ARCHITECTURE.tar.gz.sha512
shasum -a 512 -c opensearch-$VERSION-$PLATFORM-$ARCHITECTURE.tar.gz.sha512
rm -rf ${WORKING_DIR}