#!/bin/bash
# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

if (! docker stats --no-stream 2>/dev/null); then
    if [ "$(uname)" == "Darwin" ]; then #Mac
        echo 'macOS'
        open /Applications/Docker.app
        echo -n "Waiting for Docker to launch"
        sleep 1
    elif [ "$(expr substr $(uname -s) 1 5)" == "Linux" ]; then #Linux
        echo 'Linux'
        sudo systemctl start docker
        echo -n "Waiting for Docker to launch"
        sleep 1
    fi
  # Wait until Docker daemon is running and has completed initialisation
  while (! docker stats --no-stream >/dev/null 2>&1); do
    # Docker takes a few seconds to initialize
    echo -n "."
    sleep 1
  done
fi
echo
echo "Docker started"