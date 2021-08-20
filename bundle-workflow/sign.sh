#!/bin/bash

set -e

DIR="$(dirname "$0")"
python3 "$DIR/python/sign.py" $@
