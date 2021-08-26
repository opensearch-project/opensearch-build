#!/bin/bash

set -e

DIR="$(dirname "$0")"
"$DIR/run.sh" "$DIR/src/sign.py" $@
