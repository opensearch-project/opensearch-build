#!/bin/bash

# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

set -e

outputDir=artifacts
mkdir -p $outputDir/maven
cd notifications

./gradlew publishToMavenLocal -PexcludeTests="**/SesChannelIT*" -Dopensearch.version=$1

