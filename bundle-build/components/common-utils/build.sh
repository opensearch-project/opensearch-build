#!/bin/bash

opensearch_version=$1

./gradlew build -Dopensearch.version=$1
./gradlew publishToMavenLocal -Dopensearch.version=$1
mkdir -p common-utils-artifacts/maven
cp -r ~/.m2/repository/org/opensearch/common-utils common-utils-artifacts/maven
