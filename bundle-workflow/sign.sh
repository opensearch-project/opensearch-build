#!/bin/bash

set -e

DIR="$(dirname "$0")"
"$DIR/run.sh" "$DIR/python/sign.py" $@
