#!/bin/bash

# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

set -e

# remove this script when https://github.com/opensearch-project/performance-analyzer/issues/44 is fixed
git fetch origin main
git checkout main

./gradlew build -x test
./gradlew publishToMavenLocal
