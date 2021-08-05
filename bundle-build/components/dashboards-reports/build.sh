#!/bin/bash

outputDir=$(basename $PWD)-artifacts
mkdir $outputDir
cd reports-scheduler
./gradlew assemble --no-daemon --refresh-dependencies -Dbuild.snapshot=false -DskipTests=true -Dopensearch.version=$1

distributions=$(find . -path \*build/distributions)

cp ${distributions}/*.zip ../$outputDir

