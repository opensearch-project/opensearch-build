#!/bin/bash

outputDir=artifacts
mkdir -p $outputDir
cd reports-scheduler
./gradlew assemble --no-daemon --refresh-dependencies -Dbuild.snapshot=false -DskipTests=true -Dopensearch.version=$1

distributions=$(find . -path \*build/distributions)
mkdir -p $outputDir/plugins
cp ${distributions}/*.zip ../$outputDir/plugins

