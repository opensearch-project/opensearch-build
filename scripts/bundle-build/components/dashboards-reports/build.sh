#!/bin/bash

cd reports-scheduler
./gradlew assemble --no-daemon --refresh-dependencies -Dbuild.snapshot=false -DskipTests=true -Dopensearch.version=$1

outputDir=../artifacts
mkdir -p $outputDir

zipPath=$(find . -path \*build/distributions/*.zip)
distributions="$(dirname "${zipPath}")"

echo "COPY ${distributions}/*.zip"
mkdir -p $outputDir/plugins
cp ${distributions}/*.zip $outputDir/plugins
