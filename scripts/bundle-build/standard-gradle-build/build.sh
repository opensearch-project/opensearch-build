#!/bin/bash

outputDir=$(basename $PWD)-artifacts
mkdir $outputDir
./gradlew assemble --no-daemon --refresh-dependencies -Dbuild.snapshot=false -DskipTests=true -Dopensearch.version=$1

zipPath=$(find . -path \*build/distributions/*.zip)
distributions="$(dirname "${zipPath}")"

echo "COPY ${distributions}/*.zip"
cp ${distributions}/*.zip ./$outputDir
