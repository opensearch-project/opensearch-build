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
    echo "Error: You must specify the OpenSearch version"
    usage
    exit 1
fi

[ -z "$OUTPUT" ] && OUTPUT=artifacts

mkdir -p $OUTPUT/maven/org/opensearch

# Build project and publish to maven local.
./gradlew publishToMavenLocal -Dbuild.snapshot=$SNAPSHOT

# Publish to existing test repo, using this to stage release versions of the artifacts that can be released from the same build.
./gradlew publishNebulaPublicationToTestRepository -Dbuild.snapshot=$SNAPSHOT

# Copy maven publications to be promoted
cp -r ./build/local-test-repo/org/opensearch "${OUTPUT}"/maven/org

# Assemble distribution artifact
# see https://github.com/opensearch-project/OpenSearch/blob/main/settings.gradle#L34 for other distribution targets

[ -z "$PLATFORM" ] && PLATFORM=$(uname -s | awk '{print tolower($0)}')
[ -z "$ARCHITECTURE" ] && ARCHITECTURE=`uname -m`

case $PLATFORM in
    linux*)
        PACKAGE="tar"
        EXT="tar.gz"
        ;;
    darwin*)
        PACKAGE="tar"
        EXT="tar.gz"
        ;;
    windows*)
        PACKAGE="zip"
        EXT="zip"
        ;;
    *)
        echo "Unsupported platform: $PLATFORM"
        exit 1
        ;;
esac

case $ARCHITECTURE in
    x64)
        TARGET="$PLATFORM-$PACKAGE"
        QUALIFIER="$PLATFORM-x64"
        ;;
    arm64)
        TARGET="$PLATFORM-arm64-$PACKAGE"
        QUALIFIER="$PLATFORM-arm64"
        ;;
    *)
        echo "Unsupported architecture: $ARCHITECTURE"
        exit 1
        ;;
esac

./gradlew :distribution:archives:$TARGET:assemble -Dbuild.snapshot=$SNAPSHOT

# Copy artifact to dist folder in bundle build output
[[ "$SNAPSHOT" == "true" ]] && IDENTIFIER="-SNAPSHOT"
ARTIFACT_BUILD_NAME=`ls distribution/archives/$TARGET/build/distributions/ | grep "opensearch-min.*$QUALIFIER.$EXT"`
mkdir -p "${OUTPUT}/dist"
cp distribution/archives/$TARGET/build/distributions/$ARTIFACT_BUILD_NAME "${OUTPUT}"/dist/$ARTIFACT_BUILD_NAME

echo "Building core plugins..."
mkdir -p "${OUTPUT}/core-plugins"
cd plugins
../gradlew assemble -Dbuild.snapshot="$SNAPSHOT"
cd ..
for plugin in plugins/*; do
  PLUGIN_NAME=$(basename "$plugin")
  if [ -d "$plugin" ] && [ "examples" != "$PLUGIN_NAME" ]; then
    PLUGIN_ARTIFACT_BUILD_NAME=`ls "$plugin"/build/distributions/ | grep "$PLUGIN_NAME.*$IDENTIFIER.zip"`
    cp "$plugin"/build/distributions/"$PLUGIN_ARTIFACT_BUILD_NAME" "${OUTPUT}"/core-plugins/"$PLUGIN_ARTIFACT_BUILD_NAME"
  fi
done
