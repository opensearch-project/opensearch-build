#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

echo "Run systemd integTest for OpenSearch core engine"
./gradlew qa:systemd-test:integTest --tests org.opensearch.systemdinteg.SystemdIT --console=plain
