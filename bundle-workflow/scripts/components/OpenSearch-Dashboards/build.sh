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
    echo -e "-a ARCHITECTURE\t[Optional] Build architecture, ignored."
    echo -e "-o OUTPUT\t[Optional] Output path, default is 'artifacts'."
    echo -e "-d DASHBOARDS\t[Optional] Build OpenSearch Dashboards, default is 'false'."
    echo -e "-h help"
}

while getopts ":h:v:s:o:a:d:" arg; do
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
        a)
            ARCHITECTURE=$OPTARG
            ;;
        d)
            DASHBOARDS=$OPTARG
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

# Assemble distribution artifact
# see https://github.com/opensearch-project/OpenSearch/blob/main/settings.gradle#L34 for other distribution targets
case $ARCHITECTURE in
    x64)
        TARGET="linux-tar"
        QUALIFIER="linux-x64"
        ;;
    arm64)
        TARGET="linux-arm64-tar"
        QUALIFIER="linux-arm64"
        ;;
    *)
        echo "Unsupported architecture: ${ARCHITECTURE}"
        exit 1
        ;;
esac

echo "Building node modules for core"
yarn osd bootstrap

echo "Building artifact"
if [ "$SNAPSHOT" = "true" ]
then
    IDENTIFIER="-SNAPSHOT"
    yarn build --skip-os-packages
else
    yarn build --skip-os-packages --release
fi

mkdir -p "${OUTPUT}/bundle"
# Copy artifact to bundle output with -min in the name
ARTIFACT_BUILD_NAME=opensearch-dashboards-$VERSION$IDENTIFIER-$QUALIFIER.tar.gz
ARTIFACT_TARGET_NAME=opensearch-dashboards-min-$VERSION$IDENTIFIER-$QUALIFIER.tar.gz
cp target/$ARTIFACT_BUILD_NAME $OUTPUT/bundle/$ARTIFACT_TARGET_NAME