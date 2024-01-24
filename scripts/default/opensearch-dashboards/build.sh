#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

set -ex

# vars / libs
SCRIPT_DIR=`dirname $(realpath $0)`
. $SCRIPT_DIR/../../../lib/shell/file_management.sh
PLUGIN_NAME=$(basename "$PWD")
PLUGIN_PATH=`realpath ../OpenSearch-Dashboards/plugins/$PLUGIN_NAME`

function usage() {
    echo "Usage: $0 [args]"
    echo ""
    echo "Arguments:"
    echo -e "-v VERSION\t[Required] OpenSearch version."
    echo -e "-q QUALIFIER\t[Optional] Version qualifier."
    echo -e "-s SNAPSHOT\t[Optional] Build a snapshot, default is 'false'."
    echo -e "-p PLATFORM\t[Optional] Platform, ignored."
    echo -e "-a ARCHITECTURE\t[Optional] Build architecture, ignored."
    echo -e "-o OUTPUT\t[Optional] Output path, default is 'artifacts'."
    echo -e "-h help"
}


function cleanup_all() {
    File_Delete $PLUGIN_PATH
}

trap cleanup_all TERM INT EXIT

while getopts ":h:v:q:s:o:p:a:" arg; do
    case $arg in
        h)
            usage
            exit 1
            ;;
        v)
            VERSION=$OPTARG
            ;;
        q)
            QUALIFIER=$OPTARG
            ;;
        s)
            SNAPSHOT=$OPTARG
            ;;
        o)
            OUTPUT=$OPTARG
            ;;
        p)
            PLATFORM=$OPTARG
            ;;
        a)
            ARCHITECTURE=$OPTARG
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

if [ -z "$VERSION" ]; then
    echo "Error: You must specify the OpenSearch Dashboards version"
    usage
    exit 1
fi

[ -z "$OUTPUT" ] && OUTPUT=artifacts
[ ! -z "$QUALIFIER" ] && QUALIFIER_IDENTIFIER="-$QUALIFIER"

NVM_CMD="source $NVM_DIR/nvm.sh && nvm use"
if [ "$PLATFORM" = "windows" ]; then
    NVM_CMD="volta install node@`cat ../OpenSearch-Dashboards/.nvmrc` && volta install yarn@`jq -r '.engines.yarn' ../OpenSearch-Dashboards/package.json`"
fi

HELPER_CMD=$(jq -r '.scripts.plugin_helpers' package.json)
if [ "$HELPER_CMD" != null ]; then
    HELPER_STRING=plugin_helpers
else
    HELPER_STRING=plugin-helpers
fi

mkdir -p $OUTPUT/plugins
# TODO: [CLEANUP] Needed OpenSearch Dashboards git repo to build the required modules for plugins
# This makes it so there is a dependency on having Dashboards pulled already.
cp -r ../$PLUGIN_NAME/ ../OpenSearch-Dashboards/plugins
echo "BUILD MODULES FOR $PLUGIN_NAME"
CURR_DIR=`pwd`
cd ../OpenSearch-Dashboards; eval $NVM_CMD; yarn osd bootstrap
echo "BUILD RELEASE ZIP FOR $PLUGIN_NAME"
cd plugins/$PLUGIN_NAME; yarn $HELPER_STRING build --opensearch-dashboards-version=$VERSION$QUALIFIER_IDENTIFIER
cd $CURR_DIR
echo "COPY $PLUGIN_NAME.zip"
cp -r ../OpenSearch-Dashboards/plugins/$PLUGIN_NAME/build/$PLUGIN_NAME-$VERSION$QUALIFIER_IDENTIFIER.zip $OUTPUT/plugins/
