#!/bin/bash

# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

set -ex

function usage() {
    echo "Usage: $0 [args]"
    echo ""
    echo "Arguments:"
    echo -e "-v VERSION\t[Required] OpenSearch Dashboards version."
    echo -e "-q QUALIFIER\t[Optional] Version qualifier."
    echo -e "-s SNAPSHOT\t[Optional] Build a snapshot, default is 'false'."
    echo -e "-p PLATFORM\t[Optional] Platform, default is 'uname -s'."
    echo -e "-a ARCHITECTURE\t[Optional] Build architecture, default is 'uname -m'."
    echo -e "-d DISTRIBUTION\t[Optional] Distribution, default is 'tar'."
    echo -e "-o OUTPUT\t[Optional] Output path, default is 'artifacts'."
    echo -e "-h help"
}

while getopts ":h:v:q:s:o:p:a:d:" arg; do
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
        d)
            DISTRIBUTION=$OPTARG
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
[ -z "$DISTRIBUTION" ] && DISTRIBUTION="tar"
[ ! -z "$QUALIFIER" ] && QUALIFIER_IDENTIFIER="-$QUALIFIER"
[[ "$SNAPSHOT" == "true" ]] && IDENTIFIER="-SNAPSHOT"
[[ "$SNAPSHOT" != "true" ]] && RELEASE="--release"

# Assemble distribution artifact
# see https://github.com/opensearch-project/OpenSearch/blob/main/settings.gradle#L34 for other distribution targets
case $PLATFORM-$DISTRIBUTION-$ARCHITECTURE in
    linux-tar-x64)
        TARGET="--$PLATFORM"
        EXT="tar.gz"
        BUILD_PARAMS="build-platform"
        EXTRA_PARAMS="--skip-os-packages"
        SUFFIX="$PLATFORM-x64"
        ;;
    linux-tar-arm64)
        TARGET="--$PLATFORM-arm"
        EXT="tar.gz"
        BUILD_PARAMS="build-platform"
        EXTRA_PARAMS="--skip-os-packages"
        SUFFIX="$PLATFORM-arm64"
        ;;
    windows-zip-x64)
        TARGET="--windows"
        EXT="$DISTRIBUTION"
        BUILD_PARAMS="build-platform"
        EXTRA_PARAMS="--skip-os-packages"
        SUFFIX="$PLATFORM-x64"
        ;;
    linux-deb-arm64)
        TARGET="--$DISTRIBUTION-arm"
        EXT="$DISTRIBUTION"
        BUILD_PARAMS="build"
        EXTRA_PARAMS="--skip-archives"
        SUFFIX="arm64"
        ;;
    linux-deb-x64)
        TARGET="--$DISTRIBUTION"
        EXT="$DISTRIBUTION"
        BUILD_PARAMS="build"
        EXTRA_PARAMS="--skip-archives"
        SUFFIX="amd64"
        ;;
    linux-rpm-x64)
        TARGET="--$DISTRIBUTION"
        EXT="$DISTRIBUTION"
        BUILD_PARAMS="build"
        EXTRA_PARAMS="--skip-archives"
        SUFFIX="x64"
        ;;
    linux-rpm-arm64)
        TARGET="--$DISTRIBUTION-arm"
        EXT="$DISTRIBUTION"
        BUILD_PARAMS="build"
        EXTRA_PARAMS="--skip-archives"
        SUFFIX="arm64"
        ;;
    *)
        echo "Unsupported platform-distribution-architecture combination: $PLATFORM-$DISTRIBUTION-$ARCHITECTURE"
        exit 1
        ;;
esac

NVM_CMD="source $NVM_DIR/nvm.sh && nvm use"
if [ "$PLATFORM" = "windows" ]; then
    NVM_CMD="volta install node@`cat .nvmrc` && volta install yarn@`jq -r '.engines.yarn' package.json`"
fi

eval $NVM_CMD

echo "Building node modules for core with $PLATFORM-$DISTRIBUTION-$ARCHITECTURE"
yarn osd bootstrap

echo "Building artifact"

yarn $BUILD_PARAMS $TARGET $EXTRA_PARAMS $RELEASE --version-qualifier=$QUALIFIER

mkdir -p "${OUTPUT}/dist"
# Copy artifact to dist folder in bundle build output
ARTIFACT_BUILD_NAME=opensearch-dashboards-$VERSION$QUALIFIER_IDENTIFIER$IDENTIFIER-$SUFFIX.$EXT
ARTIFACT_TARGET_NAME=opensearch-dashboards-min-$VERSION$QUALIFIER_IDENTIFIER$IDENTIFIER-$SUFFIX.$EXT
cp target/$ARTIFACT_BUILD_NAME $OUTPUT/dist/$ARTIFACT_TARGET_NAME
