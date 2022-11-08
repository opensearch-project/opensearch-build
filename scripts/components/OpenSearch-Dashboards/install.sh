#!/bin/bash

# Copyright OpenSearch Contributors
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
    echo -e "-v VERSION\t[Required] OpenSearch version."
    echo -e "-s SNAPSHOT\t[Optional] Build a snapshot, default is 'false'."
    echo -e "-p PLATFORM\t[Optional] Platform, default is 'uname -s'."
    echo -e "-a ARCHITECTURE\t[Optional] Build architecture, default is 'uname -m'."
    echo -e "-d DISTRIBUTION\t[Optional] Distribution, default is 'tar'."
    echo -e "-f ARTIFACTS\t[Optional] Location of build artifacts."
    echo -e "-o OUTPUT\t[Optional] Output path."
    echo -e "-h help"
}

while getopts ":h:v:s:o:p:a:d:f:" arg; do
    case $arg in
        h)
            usage
            exit 1
            ;;
        v)
            VERSION=$OPTARG
            ;;
        s)
            SNAPSHOT=$OPTARG
            ;;
        o)
            OUTPUT=$OPTARG
            ;;
        p)
            PLATFORM=$OPTARG
            ;;
        a)
            ARCHITECTURE=$OPTARG
            ;;
        d)
            DISTRIBUTION=$OPTARG
            ;;
        f)
            ARTIFACTS=$ARTIFACTS
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

if [ -z "$VERSION" ]; then
    echo "Error: missing version."
    usage
    exit 1
fi

[ -z "$SNAPSHOT" ] && SNAPSHOT="false"
[ -z "$PLATFORM" ] && PLATFORM=$(uname -s | awk '{print tolower($0)}')
[ -z "$ARCHITECTURE" ] && ARCHITECTURE=`uname -m`
[ -z "$DISTRIBUTION" ] && DISTRIBUTION="tar"

# Make sure the cwd is where the script is located
DIR="$(dirname "$0")"
echo $DIR
cd $DIR

## Setup default config

MAJOR_VERSION=`echo $VERSION | cut -d. -f1`
if ! (ls ../../../config/ | grep -E "opensearch_dashboards-.*.x.yml" | grep $MAJOR_VERSION); then
    MAJOR_VERSION="default"
fi

if [ "$DISTRIBUTION" = "rpm" ]; then
    cp -v ../../../config/opensearch_dashboards-$MAJOR_VERSION.x.yml "$OUTPUT/../etc/opensearch-dashboards/opensearch_dashboards.yml"
    cp -a ../../../scripts/pkg/service_templates/opensearch-dashboards/* "$OUTPUT/../"
    cp -a ../../../scripts/pkg/build_templates/opensearch-dashboards/* "$OUTPUT/../"
else
    cp -v ../../../config/opensearch_dashboards-$MAJOR_VERSION.x.yml "$OUTPUT/config/opensearch_dashboards.yml"
fi
