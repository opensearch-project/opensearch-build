#!/bin/bash

# remove this script when https://github.com/opensearch-project/performance-analyzer/issues/44 is fixed
git fetch origin main
git checkout main

./gradlew build -x test
./gradlew publishToMavenLocal
