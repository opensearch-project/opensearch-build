#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

set -ex

function usage() {
    echo "Usage: $0 [args]"
    echo ""
    echo "Arguments:"
    echo -e "-v VERSION\t[Required] OpenSearch version."
    echo -e "-s SNAPSHOT\t[Optional] Build a snapshot, default is 'false'."
    echo -e "-p PLATFORM\t[Optional] Platform, default is 'uname -s'."
    echo -e "-a ARCHITECTURE\t[Optional] Build architecture, default is 'uname -m'."
    echo -e "-o OUTPUT\t[Optional] Output path, default is 'artifacts'."
    echo -e "-h help"
}

while getopts ":h:v:s:o:p:a:" arg; do
    case $arg in
        h)
            usage
            exit 1
            ;;
        v)
            VERSION=$OPTARG
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
[ -z "$PLATFORM" ] && PLATFORM=$(uname -s | awk '{print tolower($0)}')
[ -z "$ARCHITECTURE" ] && ARCHITECTURE=`uname -m`

case $PLATFORM in
    linux*)
        PLATFORM="linux"
        ;;
    *)
        echo "Unsupported platform: $PLATFORM"
        exit 1
        ;;
esac

case $ARCHITECTURE in
    x64|arm64)
        CHROMIUM_TARGET="chromium-$PLATFORM-$ARCHITECTURE.zip"
        ;;
    *)
        echo "Unsupported architecture: $ARCHITECTURE"
        exit 1
        ;;
esac

CHROMIUM_URL="https://github.com/opensearch-project/dashboards-reports/releases/download/chromium-1.12.0.0/$CHROMIUM_TARGET"

mkdir -p $OUTPUT/plugins
# For hybrid plugin it actually resides in 'reportsDashboards/dashboards-reports'
PLUGIN_FOLDER=$(basename "$PWD")
PLUGIN_NAME=$(basename $(dirname "$PWD"))
# TODO: [CLEANUP] Needed OpenSearch Dashboards git repo to build the required modules for plugins
# This makes it so there is a dependency on having Dashboards pulled already.
cp -r ../$PLUGIN_FOLDER/ ../../OpenSearch-Dashboards/plugins
echo "BUILD MODULES FOR $PLUGIN_NAME"
(cd ../../OpenSearch-Dashboards && yarn osd bootstrap)
echo "BUILD RELEASE ZIP FOR $PLUGIN_NAME"
(cd ../../OpenSearch-Dashboards/plugins/$PLUGIN_FOLDER && yarn plugin_helpers build)
# Reporting uses headless chromium to generate reports, which needs to be included in its artifact
echo "DOWNLOADING CHROMIUM FOR $PLUGIN_NAME"
mkdir -p ../../OpenSearch-Dashboards/plugins/$PLUGIN_FOLDER/build/opensearch-dashboards/$PLUGIN_NAME
curl -sLO "$CHROMIUM_URL"
echo "PUTTING CHROMIUM INSIDE $PLUGIN_NAME-$VERSION.zip"
unzip "$CHROMIUM_TARGET" -d ../../OpenSearch-Dashboards/plugins/$PLUGIN_FOLDER/build/opensearch-dashboards/$PLUGIN_NAME
(cd ../../OpenSearch-Dashboards/plugins/$PLUGIN_FOLDER/build && zip -ur $PLUGIN_NAME-$VERSION.zip opensearch-dashboards)
echo "COPY $PLUGIN_NAME.zip"
cp -r ../../OpenSearch-Dashboards/plugins/$PLUGIN_FOLDER/build/$PLUGIN_NAME-$VERSION.zip $OUTPUT/plugins/
rm -rf ../../OpenSearch-Dashboards/plugins/$PLUGIN_FOLDER
