#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This script is to output yarn version properly based on the OpenSearch-Dashboards core package.json
# https://raw.githubusercontent.com/opensearch-project/OpenSearch-Dashboards/main/package.json

set -e

if [ -z "$1" ]; then
    echo "Please enter the reference (branch/tag/commitid) in OpenSearch-Dashboards core"
    exit 1
fi

ref=$1

JSON_BASE="https://raw.githubusercontent.com/opensearch-project/OpenSearch-Dashboards/${ref}/package.json"

YARN_VERSION=`curl -s -o- $JSON_BASE | yq -r '.engines.yarn'`

echo $YARN_VERSION
