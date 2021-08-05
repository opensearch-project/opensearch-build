#!/bin/bash

outputDir=$(basename $PWD)-artifacts
mkdir -p $outputDir/maven
cd notifications

./gradlew publishToMavenLocal -PexcludeTests="**/SesChannelIT*" -Dopensearch.version=$1

