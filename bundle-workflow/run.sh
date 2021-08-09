#!/bin/bash

# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

set -e

DIR="$(dirname "$0")"

if [ -z "$1" ]; then (echo "syntax: run.sh [workflow.py]"; exit -1); fi
command -v python3 >/dev/null 2>&1 || (echo "missing python3"; exit -1)
command -v pip >/dev/null 2>&1 || (echo "missing python3-pip"; exit -1)
command -v pipenv >/dev/null 2>&1 || (echo "missing pipenv"; exit -1)

python3 -m pipenv install
python3 -m pipenv run "$1" ${@:2}
