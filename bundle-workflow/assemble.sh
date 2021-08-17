#!/bin/bash

# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

set -e

DIR="$(dirname "$0")"
"$DIR/run.sh" "$DIR/python/assemble.py" $@
