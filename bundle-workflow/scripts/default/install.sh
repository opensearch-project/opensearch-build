#!/bin/bash

# SPDX-License-Identifier: Apache-2.0
#
# The OpenSearch Contributors require contributions made to
# this file be licensed under the Apache-2.0 license or a
# compatible open source license.

set -ex

function usage() {
    echo "Usage: $0 [args]"
    echo ""
    echo "Arguments:"
    echo -e "-a ARTIFACTS\t[Required] Location of build artifacts."
    echo -e "-o OUTPUT\t[Required] Output path."
    echo -e "-h help"
}

while getopts ":h:a:o:" arg; do
    case $arg in
        h)
            usage
            exit 1
            ;;
        o)
            OUTPUT=$OPTARG
            ;;
        a)
            ARTIFACTS=$OPTARG
            ;;
        ?)
            echo "Invalid option: -${arg}"
            exit 1
            ;;
    esac
done
