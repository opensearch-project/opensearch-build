#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0


#
# About:        This shell script generate an opensearch-dashboards tarball with all the provided plugins installed and ready to use.
#               It will create a folder named target that will consist of the tarball and shasum of the same.
#               A manifest file and right permissions set up is essential to download the required artifacts
# Dependencies: yq (More info: https://github.com/mikefarah/yq/tree/v4.4.1#install)
#               shasum
# Usage:        ./opensearch-dashboards-tar-build.sh -f <path/to/manifest/file/>
#

set -e

function usage() {
    echo "Usage: $0 [args]"
    echo -e "Supported manifest schema-version: 1.0"
    echo ""
    echo "Arguments:"
    echo -e "-f MANIFEST_FILE\t[Required] Path/to/manifest.yml file"
    echo -e "-h help"
}

while getopts ":hf:" arg; do
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
    echo "Error: The file '${MANIFEST_FILE}' does not exist"
    usage
    exit 1
fi

SCHEMA_VERSION=`yq eval '.manifest.schema-version' $MANIFEST_FILE`
PLATFORM=`yq eval '.build.platform' $MANIFEST_FILE`
ARCHITECTURE=`yq eval '.build.architecture' $MANIFEST_FILE`
VERSION=`yq eval '.build.version' $MANIFEST_FILE`
UNDERLYING_ARCH=`uname -p`

if [ -z "$VERSION" ]; then
    echo "Error: Please specify the version in the manifest file"
    usage
    exit 1
fi

if [ "$SCHEMA_VERSION" != "1.0" ]; then
    echo "Error: This script only supports manifest schema version 1.0, but ${MANIFEST_FILE} is version '${SCHEMA_VERSION}'"
    usage
    exit 1
fi

if [ "$PLATFORM" != "linux" ]; then
    echo "Error: $PLATFORM platform is not supported yet! Only supported platform is linux"
    usage
    exit 1
fi

if [ "$ARCHITECTURE" != "x64" ] && [ "$ARCHITECTURE" != "arm64" ]
then
    echo "Error: $ARCHITECTURE architecture is not supported yet! Only supported architectures are x64 and arm64"
    usage
    exit 1
fi

if [[ ( "$ARCHITECTURE" == "arm64" && ( "$UNDERLYING_ARCH" != "aarch64" && "$UNDERLYING_ARCH" != "arm64" )) ||  ( "$ARCHITECTURE" == "x64" && ( "$UNDERLYING_ARCH" != "x86_64" && "$UNDERLYING_ARCH" != "amd64" )) ]]
then
    echo "Error: The underlying architecture ($UNDERLYING_ARCH) does not match the product architecture($ARCHITECTURE) that you are trying to build"
    echo "To build $ARCHITECTURE you need to be on $ARCHITECTURE architecture environment"
    exit 1
fi

TARGET_DIR=`pwd`
REPO_ROOT=`git rev-parse --show-toplevel`
ROOT=`dirname $(realpath $0)`; cd $ROOT
DIR_NAME="opensearch-dashboards-$VERSION"
WORKING_DIR="$ROOT/$DIR_NAME"
PLUGINS_TEMP=`mktemp -d`
OPENSEARCH_DASHBOARDS_CORE_URL=`yq eval '.products.opensearch-dashboards.opensearch-dashboards-min' $MANIFEST_FILE | sed s/^-// | sed -e 's/^[[:space:]]*//'`
OPENSEARCH_DASHBOARDS_PLUGINS_URLS=`yq eval '.products.opensearch-dashboards.plugins' $MANIFEST_FILE | sed s/^-// | sed -e 's/^[[:space:]]*//'`

TRAP_SIG_LIST="TERM INT EXIT"
function delete_temp_folders() {
      echo "Deleting the temp folders"
      rm -rf $WORKING_DIR $PLUGINS_TEMP
}
trap delete_temp_folders $TRAP_SIG_LIST

# # Download plugins to local 
mkdir -p $WORKING_DIR
echo "working dir is: ${WORKING_DIR}"
IFS=$'\n'
for plugin in ${OPENSEARCH_DASHBOARDS_PLUGINS_URLS}; do
  aws s3 cp $plugin $PLUGINS_TEMP/
done

# Download OpenSearch Dashboards min tarball
wget -q ${OPENSEARCH_DASHBOARDS_CORE_URL} -O opensearch-dashboards.tar.gz
tar -xzf opensearch-dashboards.tar.gz --strip-components=1 --directory "$WORKING_DIR" && rm -rf opensearch-dashboards.tar.gz

# Install plugins to OpenSearch
for plugin_url in $OPENSEARCH_DASHBOARDS_PLUGINS_URLS; do
    plugin=`basename $plugin_url`
    $WORKING_DIR/bin/opensearch-dashboards-plugin --allow-root install file:$PLUGINS_TEMP/$plugin
done

echo "Plugins installed are:"
ls -tlr $WORKING_DIR/plugins

# Copy the tarball installation script 
cp $REPO_ROOT/config/opensearch_dashboards.yml $WORKING_DIR/config/

# Tar the bundle and clean up
rm -rf $PLUGINS_TEMP
cd $ROOT
echo "Generating the tarball"
tar -czf $TARGET_DIR/opensearch-dashboards-$VERSION-$PLATFORM-$ARCHITECTURE.tar.gz $DIR_NAME
cd $TARGET_DIR
shasum -a 512 opensearch-dashboards-$VERSION-$PLATFORM-$ARCHITECTURE.tar.gz > opensearch-dashboards-$VERSION-$PLATFORM-$ARCHITECTURE.tar.gz.sha512
shasum -a 512 -c opensearch-dashboards-$VERSION-$PLATFORM-$ARCHITECTURE.tar.gz.sha512