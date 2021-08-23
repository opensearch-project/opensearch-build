#!/bin/bash

# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

set -ex

function usage() {
    echo "Usage: $0 [args]"
    echo ""
    echo "Arguments:"
    echo -e "-v VERSION\t[Required] OpenSearch version."
    echo -e "-s SNAPSHOT\t[Optional] Build a snapshot, default is 'false'."
    echo -e "-a ARCHITECTURE\t[Optional] Build architecture, ignored."
    echo -e "-o OUTPUT\t[Optional] Output path, default is 'artifacts'."
    echo -e "-h help"
}

while getopts ":h:v:s:o:a:" arg; do
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

./gradlew :distribution:archives:$TARGET:assemble -Dbuild.snapshot=$SNAPSHOT

# Copy artifact to bundle output with -min in the name
[[ "$SNAPSHOT" == "true" ]] && IDENTIFIER="-SNAPSHOT"
ARTIFACT_BUILD_NAME=opensearch-$VERSION$IDENTIFIER-$QUALIFIER.tar.gz
ARTIFACT_TARGET_NAME=opensearch-min-$VERSION$IDENTIFIER-$QUALIFIER.tar.gz
mkdir -p "${OUTPUT}/bundle"
cp distribution/archives/$TARGET/build/distributions/$ARTIFACT_BUILD_NAME "${OUTPUT}"/bundle/$ARTIFACT_TARGET_NAME

echo "Building core plugins..."
mkdir -p "${OUTPUT}/core-plugins"
cd plugins
../gradlew assemble -Dbuild.snapshot="$SNAPSHOT"
cd ..
for plugin in plugins/*; do
  PLUGIN_NAME=$(basename "$plugin")
  if [ -d "$plugin" ] && [ "examples" != "$PLUGIN_NAME" ]; then
    PLUGIN_ARTIFACT_BUILD_NAME=$PLUGIN_NAME-$VERSION$IDENTIFIER.zip
    cp "$plugin"/build/distributions/"$PLUGIN_ARTIFACT_BUILD_NAME" "${OUTPUT}"/core-plugins/"$PLUGIN_ARTIFACT_BUILD_NAME"
  fi
done
