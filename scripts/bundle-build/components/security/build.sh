#!/bin/bash

# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

set -e

mvn -B clean package -Padvanced -DskipTests
artifact_zip=$(ls $(pwd)/target/releases/opensearch-security-*.zip | grep -v admin-standalone)
./gradlew assemble --no-daemon -ParchivePath=$artifact_zip -Dbuild.snapshot=false
outputDir=artifacts
mkdir -p $outputDir/plugins
cp $artifact_zip $outputDir/plugins
