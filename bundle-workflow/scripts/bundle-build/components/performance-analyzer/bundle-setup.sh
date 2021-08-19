#!/bin/bash

# Copyright OpenSearch Contributors.
# SPDX-License-Identifier: Apache-2.0

set -ex

function usage() {
    echo "Usage: $0 [args]"
    echo ""
    echo "Arguments:"
    echo -e "-d WORKING_DIR\t[Required] path of the unpacked tar directory."
    echo -e "-l LIB_PATH\t[Optional] path of an external lib that should be installed."
    echo -e "-h help"
}

while getopts ":h:d:l:" arg; do
    case $arg in
        h)
            usage
            exit 1
            ;;
        d)
            WORKING_DIR=$OPTARG
            ;;
        l)
            LIB_PATH=$OPTARG
            ;;
        :)
            echo "Error: -${OPTARG} requires an argument"
            usage
            exit 1
            ;;
        ?)
            echo "Invalid option: -${arg}"
            exit 1
            ;;
    esac
done

if [ -z "$WORKING_DIR" ]; then
    echo "Error: You must specify the tarball directory"
    usage
    exit 1
fi

# Setup Performance Analyzer Agent
ls ..
echo "WHAT IS THERE"
cp -r $WORKING_DIR/plugins/opensearch-performance-analyzer/performance-analyzer-rca $WORKING_DIR/
chmod -R 755 $WORKING_DIR/performance-analyzer-rca
mv $WORKING_DIR/bin/opensearch-performance-analyzer/performance-analyzer-agent-cli $WORKING_DIR/bin
rm -rf $WORKING_DIR/bin/opensearch-performance-analyzer