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
        o)
            OUTPUT=$OPTARG
            ;;
        a)
            ARTIFACTS=$OPTARG
            ;;
        h)
            usage
            exit 1
            ;;
        ?)
            echo "Invalid option: -${arg}"
            exit 1
            ;;
    esac
done

# see https://github.com/opensearch-project/k-NN/issues/80 to make this part of the plugin installer
echo "Copying libKNN from $ARTIFACTS to $OUTPUT ..."
mkdir -p "$OUTPUT/plugins/opensearch-knn/knnlib"
cp "$ARTIFACTS"/libs/lib*knn* "$ARTIFACTS"/libs/lib*KNN* "$OUTPUT/plugins/opensearch-knn/knnlib"
