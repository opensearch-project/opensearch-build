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

outputDir=$OUTPUT
mkdir -p "${outputDir}/maven"

# Build project and publish to maven local.
./gradlew publishToMavenLocal -Dbuild.snapshot=$SNAPSHOT

# Publish to existing test repo, using this to stage release versions of the artifacts that can be released from the same build.
./gradlew publishNebulaPublicationToTestRepository -Dbuild.snapshot=$SNAPSHOT

# Copy maven publications to be promoted
cp -r ./build/local-test-repo/org/opensearch "${outputDir}"/maven

if [ "${ARCHITECTURE}" = "x64" ]; then
  ./gradlew :distribution:archives:linux-tar:assemble -Dbuild.snapshot=false
  cp -r distribution/archives/linux-tar/build/distributions/. "${outputDir}"/bundle
elif [ "${ARCHITECTURE}" == "arm64" ]; then
  ./gradlew :distribution:archives:linux-arm64-tar:assemble -Dbuild.snapshot=false
  cp -r distribution/archives/linux-arm64-tar/build/distributions/ "${outputDir}"/bundle
fi

cd $outputDir/bundle

#rename included bundle to -min.
ARTIFACT_FULL_NAME=`ls  | grep -E 'tar.gz$' | tail -n 1`
ARTIFACT_BASE_NAME=`basename -s .tar.gz $ARTIFACT_FULL_NAME | sed "s/opensearch/opensearch-min/g"`
ARTIFACT_NEW_NAME="${ARTIFACT_BASE_NAME}${IDENTIFIER}.tar.gz"
mv $ARTIFACT_FULL_NAME $ARTIFACT_NEW_NAME || true
