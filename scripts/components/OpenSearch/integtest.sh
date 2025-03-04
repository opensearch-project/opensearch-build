#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

set -e

echo "Check if distribution is deb or rpm on linux"
if [ "$OSTYPE" = "linux-gnu" ]; then
    if (dpkg -s opensearch > /dev/null 2>&1) || (rpm -q opensearch > /dev/null 2>&1); then
        echo "Run systemd integTest for OpenSearch core engine"
        ./gradlew :qa:systemd-test:test --tests org.opensearch.systemdinteg.SystemdIntegTests --console=plain
    else
        echo "No deb or rpm installed detected, skip test"
    fi
else
    echo "Not on linux host, skip test"
fi

exit 0
