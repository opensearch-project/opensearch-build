#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

# This script is used as an entrypoint to switch nvm version

source $NVM_DIR/nvm.sh
nvm install $NODE_VERSION
nvm use $NODE_VERSION
bash
