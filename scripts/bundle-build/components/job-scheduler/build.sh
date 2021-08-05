#!/bin/bash

opensearch_version=$1

outputDir=artifacts
mkdir -p $outputDir
./gradlew assemble --no-daemon --refresh-dependencies -Dbuild.snapshot=false -DskipTests=true -Dopensearch.version=$1

zipPath=$(find . -path \*build/distributions/*.zip)
distributions="$(dirname "${zipPath}")"

echo "COPY ${distributions}/*.zip"
mkdir -p $outputDir/plugins
cp ${distributions}/*.zip ./$outputDir/plugins

./gradlew publishToMavenLocal -Dopensearch.version=$1 -Dbuild.snapshot=false
mkdir -p $outputDir/maven
cp -r ~/.m2/repository/org/opensearch/opensearch-job-scheduler $outputDir/maven
cp -r ~/.m2/repository/org/opensearch/opensearch-job-scheduler-spi $outputDir/maven
