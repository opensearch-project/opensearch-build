#!/bin/bash

# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

set -e

./gradlew build -x test
./gradlew publishToMavenLocal
