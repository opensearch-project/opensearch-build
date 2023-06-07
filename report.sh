#!/bin/bash

# Copyright OpenSearch Contributors
# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

set -e

DIR="$(dirname "$0")"
case $1 in
  "test-run")
  "$DIR/run.sh" "$DIR/src/run_test_report.py" "${@:2}"
  ;;
  *)
  echo "Invalid report command, run ./report.sh test-run."
  exit 1
  ;;
esac

