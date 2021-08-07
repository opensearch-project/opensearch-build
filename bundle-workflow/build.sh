#!/bin/bash

# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

set -e

DIR="$(dirname "$0")"
python3 "$DIR/python/build.py" $@
