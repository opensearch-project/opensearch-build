#!/bin/bash

outputDir=artifacts
mkdir -p $outputDir/maven
cd notifications

./gradlew publishToMavenLocal -PexcludeTests="**/SesChannelIT*" -Dopensearch.version=$1

