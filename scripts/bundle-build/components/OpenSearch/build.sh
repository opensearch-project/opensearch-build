#!/bin/bash

set -e

version="$1"
ARCHITECTURE="$2"

outputDir=artifacts
mkdir -p "${outputDir}/maven"

# Build project and publish to maven local.
./gradlew publishToMavenLocal -Dbuild.snapshot=false

# Publish to existing test repo, using this to stage release versions of the artifacts that can be released from the same build.
./gradlew publishNebulaPublicationToTestRepository -Dbuild.snapshot=false

# Copy maven publications to be promoted
cp -r ./build/local-test-repo/org/opensearch "${outputDir}"/maven

if [ "${ARCHITECTURE}" = "x64" ]
then
  ./gradlew :distribution:archives:linux-tar:assemble -Dbuild.snapshot=false
  cp -r distribution/archives/linux-tar/build/distributions/. "${outputDir}"/bundle
elif [ "${ARCHITECTURE}" == "arm64" ]
then
  ./gradlew :distribution:archives:linux-arm64-tar:assemble -Dbuild.snapshot=false
  cp -r distribution/archives/linux-arm64-tar/build/distributions/ "${outputDir}"/bundle
fi

cd $outputDir

#rename included bundle to -min.
ARTIFACT_FULL_NAME=`ls  | grep -E 'tar.gz$' | tail -n 1`
ARTIFACT_BASE_NAME=`basename -s .tar.gz $ARTIFACT_FULL_NAME | sed "s/opensearch/opensearch-min/g"`
ARTIFACT_NEW_NAME="${ARTIFACT_BASE_NAME}${IDENTIFIER}.tar.gz"
mv $ARTIFACT_FULL_NAME $ARTIFACT_NEW_NAME || true
