#!/bin/sh

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# Description:
# Pre-remove script to stop "<%= product %>".service if it's running.

set -e

echo -n "Stopping <%= product %> service..."
if command -v systemctl >/dev/null && systemctl is-active "<%= product %>".service >/dev/null; then
    systemctl --no-reload stop "<%= product %>".service
fi
echo " OK"
