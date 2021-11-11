#!/bin/bash

# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

set -ex

function usage() {
    echo "Usage: $0 [args]"
    echo ""
    echo "Arguments:"
    echo -e "-v VERSION\t[Required] OpenSearch Dashboards version."
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

# Assemble distribution artifact
# see https://github.com/opensearch-project/OpenSearch/blob/main/settings.gradle#L34 for other distribution targets
case $ARCHITECTURE in
    x64)
        TARGET="--$PLATFORM"
        QUALIFIER="$PLATFORM-x64"
        ;;
    arm64)
        TARGET="--$PLATFORM-arm"
        QUALIFIER="$PLATFORM-arm64"
        ;;
    *)
        echo "Unsupported architecture: ${ARCHITECTURE}"
        exit 1
        ;;
esac

echo "Building node modules for core"
yarn osd bootstrap

echo "Building artifact"
[[ "$SNAPSHOT" == "true" ]] && IDENTIFIER="-SNAPSHOT"
[[ "$SNAPSHOT" != "true" ]] && RELEASE="--release"

yarn build-platform $TARGET --skip-os-packages $RELEASE

mkdir -p "${OUTPUT}/dist"
# Copy artifact to dist folder in bundle build output
ARTIFACT_BUILD_NAME=opensearch-dashboards-$VERSION$IDENTIFIER-$QUALIFIER.tar.gz
ARTIFACT_TARGET_NAME=opensearch-dashboards-min-$VERSION$IDENTIFIER-$QUALIFIER.tar.gz
cp target/$ARTIFACT_BUILD_NAME $OUTPUT/dist/$ARTIFACT_TARGET_NAME
