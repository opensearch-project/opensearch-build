#!/bin/bash

opensearch_version=$1

outputDir=$(basename $PWD)-artifacts
mkdir $outputDir
./gradlew assemble --no-daemon --refresh-dependencies -Dbuild.snapshot=false -DskipTests=true -Dopensearch.version=$1

zipPath=$(find . -path \*build/distributions/*.zip)
distributions="$(dirname "${zipPath}")"

echo "COPY ${distributions}/*.zip"
cp ${distributions}/*.zip ./$outputDir

./gradlew publishToMavenLocal -Dopensearch.version=$1 -Dbuild.snapshot=false
mkdir -p job-scheduler-artifacts/maven
cp -r ~/.m2/repository/org/opensearch/opensearch-job-scheduler job-scheduler-artifacts/maven
cp -r ~/.m2/repository/org/opensearch/opensearch-job-scheduler-spi job-scheduler-artifacts/maven
